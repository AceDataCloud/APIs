#!/bin/sh
# Run in the pinned n8n image with --network none. No service credentials are used.
set -eu
evidence_dir="${N8N_EVIDENCE_DIR:-/evidence}"
mkdir -p "$evidence_dir"
n8n --version > "$evidence_dir/host-version.txt"
n8n import:workflow --input=/workspace/workflows/n8n/search-summary.json > "$evidence_dir/import.log" 2>&1
n8n export:workflow --all --output="$evidence_dir/export.json" > "$evidence_dir/export.log" 2>&1
node - "$evidence_dir/export.json" <<'JS'
const fs = require('fs');
const workflows = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
if (workflows.length !== 1 || workflows[0].id !== 'acedata-search-summary-v1' || workflows[0].active !== false)
  throw new Error('Expected one inactive imported workflow');
if (workflows[0].nodes.some(node => node.credentials && Object.keys(node.credentials).length))
  throw new Error('Unexpected saved credential reference');
JS
if n8n export:credentials --all --output="$evidence_dir/credentials.json" > "$evidence_dir/credential-check.log" 2>&1; then
  echo 'Unexpected credential export success' >&2
  exit 1
fi
test ! -e "$evidence_dir/credentials.json"
node - "$evidence_dir/credential-check.log" <<'JS'
const text = require('fs').readFileSync(process.argv[2], 'utf8');
if (!text.includes('No credentials found with specified filters')) throw new Error(text);
JS
if n8n execute --id=acedata-search-summary-v1 > "$evidence_dir/unconfigured-execution.log" 2>&1; then
  echo 'Unexpected execution success without an explicit model' >&2
  exit 1
fi
node - "$evidence_dir/unconfigured-execution.log" <<'JS'
const fs = require('fs');
const path = process.argv[2];
const text = fs.readFileSync(path, 'utf8').replace(/("resumeToken"\s*:\s*")[^"]+/g, '$1[REDACTED]');
fs.writeFileSync(path, text);
if (!text.includes('Choose your exact chat-completions model ID before running.') || /Credentials not found/i.test(text))
  throw new Error('Expected local input rejection before the HTTP credential boundary');
JS
# A synthetic model isolates missing credentials without choosing a real model.
node - "$evidence_dir/configured-no-key.json" <<'JS'
const fs = require('fs');
const workflow = JSON.parse(fs.readFileSync('/workspace/workflows/n8n/search-summary.json', 'utf8'));
workflow.nodes.find(n => n.name === 'Set research input').parameters.assignments.assignments
  .find(a => a.name === 'model').value = 'credential-boundary-only';
fs.writeFileSync(process.argv[2], JSON.stringify(workflow));
JS
n8n import:workflow --input="$evidence_dir/configured-no-key.json" > "$evidence_dir/fixture-import.log" 2>&1
if n8n execute --id=acedata-search-summary-v1 > "$evidence_dir/no-key-execution.log" 2>&1; then
  echo 'Unexpected execution success without credentials' >&2
  exit 1
fi
node - "$evidence_dir/no-key-execution.log" <<'JS'
const fs = require('fs');
const path = process.argv[2];
const text = fs.readFileSync(path, 'utf8').replace(/("resumeToken"\s*:\s*")[^"]+/g, '$1[REDACTED]');
fs.writeFileSync(path, text);
if (!/Credentials not found|does not have any credentials set|credentials? (?:is|are) (?:not set|missing)/i.test(text))
  throw new Error('Expected a missing-credential failure; inspect the sanitized execution log');
fs.writeFileSync('/evidence/receipt.json', JSON.stringify({host:'n8n 2.43.7',
  network:'Docker --network none', importedInactive:true, savedCredentials:0,
  unconfigured:'rejected locally before search',
  configuredNoKey:'failed at required credential boundary', serviceRequests:0,
  paidCalls:0, fullResearchRun:'not tested'}, null, 2) + '\n');
JS
