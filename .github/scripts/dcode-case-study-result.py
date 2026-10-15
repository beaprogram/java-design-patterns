"""Print only the commit and gate result; fail closed during the experiment."""
import json
import os
from pathlib import Path

response = json.loads((Path(os.environ['RUNNER_TEMP']) / 'dcode-response.json').read_text())
gate = response.get('architecture_gate', {})
print('Commit:', os.environ['GITHUB_SHA'])
print('Architecture gate:', json.dumps(gate))
mode = os.environ.get('DCODE_ENFORCE_ARCH', '')
if mode == 'false':
    print('BOOTSTRAP ONLY: not a paper experiment result; architecture enforcement disabled.')
elif mode != 'true':
    raise SystemExit('Set DCODE_ENFORCE_ARCH explicitly to true, or false only for bootstrap.')
elif not gate.get('is_active'):
    raise SystemExit('Architecture must be active for the case study.')
elif gate.get('result') != 'PASSED':
    raise SystemExit('Architecture gate did not pass: ' + str(gate.get('result')))
