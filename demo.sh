#!/bin/bash

cp -R demo_dir /tmp/demo_dir

echo "[+] Before removal"
ls -l /tmp/demo_dir

python3 disallowed_chars_remover.py /tmp/demo_dir

echo "[+] After removal"
ls -l /tmp/demo_dir
