#!/usr/bin/env python3
"""Run unchanged, pinned Coze Studio import/mapping code without a service key."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import shutil
import subprocess
import tarfile
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
COZE = HERE.parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--archive', type=Path, required=True,
                        help='Official coze-studio source tarball at the manifest SHA.')
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--go', default='go', help='Go 1.24 executable or auto-toolchain entry point.')
    parser.add_argument('--goproxy', help='Optional Go module proxy for dependency downloads.')
    parser.add_argument('--intel-link-workaround', action='store_true',
                        help='Darwin Intel only: allow upstream Sonic runtime linknames with Go 1.24.')
    args = parser.parse_args()
    manifest = json.loads((HERE / 'upstream-sources.json').read_text())
    if args.intel_link_workaround and (platform.system(), platform.machine()) != ('Darwin', 'x86_64'):
        parser.error('--intel-link-workaround is only for the documented Darwin Intel build failure')

    with tempfile.TemporaryDirectory(prefix='coze-studio-import-') as directory:
        work = Path(directory)
        with tarfile.open(args.archive) as archive:
            members = {member.name.split('/', 1)[-1]: member
                       for member in archive.getmembers() if member.isfile()}
            for source in manifest['files']:
                member = members.get(source['path'])
                if member is None:
                    raise ValueError(f"Archive is missing {source['path']}")
                data = archive.extractfile(member).read()
                if hashlib.sha256(data).hexdigest() != source['sha256']:
                    raise ValueError(f"Pinned source hash mismatch: {source['path']}")
                target = work / Path(source['path']).relative_to('backend')
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(data)
        for name in ('go.mod', 'go.sum'):
            shutil.copy2(HERE / name, work / name)
        command = work / 'cmd/probe'
        command.mkdir(parents=True)
        shutil.copy2(HERE / 'probe.go', command / 'main.go')

        env = os.environ.copy()
        env['GOTOOLCHAIN'] = 'go1.24.0'
        if args.goproxy:
            env['GOPROXY'] = args.goproxy
        # Dependency downloads are the only network preparation. The probe
        # replaces HTTP transport and never sends fixtures to a service.
        subprocess.run([args.go, 'mod', 'download'], cwd=work, env=env, check=True)
        env['GOPROXY'] = 'off'
        files = [str(COZE / 'imports' / f'{service}.{extension}')
                 for service in ('seedance', 'happyhorse', 'nano-banana')
                 for extension in ('json', 'yaml')]
        cmd = [args.go, 'run', '-mod=readonly']
        if args.intel_link_workaround:
            cmd.append('-ldflags=-checklinkname=0')
        cmd += ['./cmd/probe', *files]
        result = subprocess.run(cmd, cwd=work, env=env, capture_output=True, text=True)
        if result.stderr:
            print(result.stderr, end='')
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(result.stdout)
        if result.returncode:
            raise SystemExit(result.returncode)
        rows = json.loads(result.stdout)
        print(f"Verified {len(rows)} files and {sum(len(row['checks']) for row in rows)} checks. "
              f"Official source: {manifest['upstream_sha']}. No service request was sent.")


if __name__ == '__main__':
    main()
