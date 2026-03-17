#!/usr/bin/env bash
set -euo pipefail

# Tworzy izolowane środowisko i instaluje zależności.
python3 -m venv env
source env/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo "\nŚrodowisko utworzone. Aktywuj je komendą: source env/bin/activate\n"
