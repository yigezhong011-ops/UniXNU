#!/usr/bin/env python3
"""Keep the link-only reference available to the board's ABI audit builders."""
import json
import os
from pathlib import Path
import shutil

root = Path(__file__).resolve().parents[2]
device = Path(os.environ['UNIXNU_DEVICE'])
source = root / 'out/fuxi/kernel/kernel.macho'
report = json.loads(source.with_suffix('.json').read_text())
assert report['original_sha256'] == 'f18b4df865405f2a287b84977d7aca745e056d656d9fc9df1662970ce2969de7'
name = 'native-owner-ufs-cpu-desktop-usb-ci-candidate.macho'
for base in (device / 'build/native-prelink', device / 'build/xnu-prelink',
             root / 'out/fuxi/tree/build/native-prelink', root / 'out/fuxi/tree/build/xnu-prelink'):
    base.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, base / name)
    shutil.copy2(source.with_suffix('.json'), (base / name).with_suffix('.json'))
print('Staged exact 21H461 link-only reference for the full build; never publish it as a phone kernel.')
