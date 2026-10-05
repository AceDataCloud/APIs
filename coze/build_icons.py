#!/usr/bin/env python3
"""Copy Studio/public service logos without publisher badges or new artwork."""
from __future__ import annotations
import argparse
import hashlib
import io
import json
import math
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.request import Request, urlopen
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--refresh', action='store_true', help='Refresh official source assets')
    args = parser.parse_args()
    sources = json.loads((ROOT / 'catalog/official-icons.json').read_text())
    originals = ROOT / 'icons/official'
    originals.mkdir(parents=True, exist_ok=True)

    def render(item):
        key, source = item
        original = originals / f'{key}.asset'
        if args.refresh or not original.exists():
            with urlopen(Request(source['url'], headers={'User-Agent': 'CozeCatalogAssetBuilder/1.0'}), timeout=30) as response:
                data = response.read()
            original.write_bytes(data)
        data = original.read_bytes()
        if b'<svg' in data[:2000]:
            import cairosvg
            data = cairosvg.svg2png(bytestring=data, output_width=512, output_height=512)
        with Image.open(io.BytesIO(data)) as image:
            image = ImageOps.exif_transpose(image).convert('RGBA')
            image.thumbnail((512, 512), Image.Resampling.LANCZOS)
            canvas = Image.new('RGBA', (512, 512), 'white')
            canvas.alpha_composite(image, ((512-image.width)//2, (512-image.height)//2))
            canvas.convert('RGB').save(ROOT / 'icons' / f'{key}.png', optimize=True)
            canvas.convert('RGB').save(ROOT / 'icons' / f'{key}.jpg', quality=96)
        return key, {'sha256': hashlib.sha256(original.read_bytes()).hexdigest(), 'source_url': source['url'], 'source': source['source']}

    with ThreadPoolExecutor(max_workers=8) as pool:
        manifest = dict(pool.map(render, sorted(sources.items())))
    (ROOT / 'catalog/official-icon-manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n')
    tile = 128
    sheet = Image.new('RGB', (tile*7, tile*math.ceil(len(sources)/7)), '#eef2f6')
    for i,key in enumerate(sorted(sources)):
        with Image.open(ROOT/'icons'/f'{key}.png') as image:
            sheet.paste(image.resize((tile,tile)),((i%7)*tile,(i//7)*tile))
    sheet.save(ROOT/'catalog/icon-contact-sheet.png')
    print(f'Prepared {len(sources)} official logos without added badges or captions.')


if __name__ == '__main__':
    main()
