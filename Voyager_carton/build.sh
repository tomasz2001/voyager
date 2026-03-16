#!/usr/bin/env bash
set -euo pipefail

source env/bin/activate

# Tworzy pojedynczy plik wykonywalny (Linux/macOS)
pyinstaller --onefile --name Voyager_carton main.py

echo "Gotowe. Sprawdź katalog dist/"