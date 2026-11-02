#!/usr/bin/env python3
"""Reject a wrong OS/device before compiling the fuxi USB build."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tomllib

root = Path(__file__).resolve().parents[2]
device = Path(os.environ['UNIXNU_DEVICE'])
board = tomllib.loads((device / 'board.toml').read_text())
ipsw = board['ipsw']
assert board.get('schema_version', 1) == 1, 'Keep the old format-1 board'
assert board['board']['name'] == 'fuxi'
assert (ipsw['product'], ipsw['version'], ipsw['build'], ipsw['device_class']) == ('iPad7,1', '17.7.11', '21H461', 'j120ap')
assert board['kernel']['prelink']['kernelcache_sha256'] == 'f18b4df865405f2a287b84977d7aca745e056d656d9fc9df1662970ce2969de7'
usb = device / 'drivers/QcomXnuUsbDebug'
revision = subprocess.check_output(['git', '-C', str(usb), 'rev-parse', 'HEAD'], text=True).strip()
assert revision == '83be5782ad7227d7d245862ce1ae3272cae14242'
assert (device / 'scripts/prepare-fuxi-usb-debug.py').is_file()
assert not (device / 'patches/xnu/zzzd-fuxi-usb-debug.patch').exists(), 'Do not stack two USB singletons'
record = dict(framework_revision=subprocess.check_output(['git', '-C', str(root), 'rev-parse', 'HEAD'], text=True).strip(),
              device_revision=subprocess.check_output(['git', '-C', str(device), 'rev-parse', 'HEAD'], text=True).strip(),
              device_repository='Kerfand/unixnu-fuxi0721', device_branch='old',
              os=ipsw, usb_revision=revision, xnu_revision='d8b80295118ef25ac3a784134bcf95cd8e88109f',
              profile='darwin23-fuxi', global_smmu_bypass=False,
              exact_stream_patch_sha256=hashlib.sha256((device / 'scripts/fuxi-usb-exact-stream.patch').read_bytes()).hexdigest(),
              hardware_verified=False)
out = root / 'out/fuxi17-usb'
out.mkdir(parents=True, exist_ok=True)
(out / 'sources.json').write_text(json.dumps(record, indent=2) + '\n')
print(json.dumps(record, indent=2))
