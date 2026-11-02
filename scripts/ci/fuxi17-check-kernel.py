#!/usr/bin/env python3
"""Require the USB driver in the full (not link-only bootstrap) kernel."""
import hashlib
import json
from pathlib import Path
import subprocess

root = Path(__file__).resolve().parents[2]
kernel = root / 'out/fuxi/kernel/kernel.macho'
raw = subprocess.check_output(['llvm-nm', '--defined-only', str(kernel)], text=True)
names = {line.split()[-1] for line in raw.splitlines() if line.split()}
required = ['_qcom_usb_debug_init', '_qcom_usb_debug_write', '_qcom_usb_debug_poll',
            '_qcom_usb_debug_panic_prepare', '_qcom_usb_debug_panic_drain']
missing = sorted(set(required) - names)
if missing:
    raise SystemExit('Full kernel missing USB implementation: ' + ', '.join(missing))
report = dict(kernel_sha256=hashlib.sha256(kernel.read_bytes()).hexdigest(),
              usb_symbols=required, os_build='21H461', hardware_verified=False,
              bootstrap_reference_delivered=False)
(root / 'out/fuxi17-usb/linked-usb.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))
