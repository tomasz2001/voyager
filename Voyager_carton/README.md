# Voyager_carton

Lekka aplikacja desktopowa w Pythonie do przesyłania i pobierania plików z canisterów na Internet Computer (ICP).

## ✅ Co jest w tym katalogu

- `main.py` — prosty interfejs GUI (Tkinter) do zarządzania plikami w canisterach
- `v_file.py` — logika przesyłania / pobierania plików do/z canistera
- `requirements.txt` — zależności Pythona
- `setup_env.sh` — tworzy izolowane środowisko (virtualenv) i instaluje zależności
- `run.sh` — uruchamia aplikację w środowisku wirtualnym
- `build.sh` — tworzy pojedynczy plik wykonywalny (opcjonalnie)

## 🧪 Jak uruchomić (bez zaśmiecania systemu)

1. Przejdź do katalogu `Voyager_carton`:

   ```sh
   cd Voyager_carton
   ```

2. Stwórz i aktywuj środowisko wirtualne oraz zainstaluj zależności:

   ```sh
   ./setup_env.sh
   ```

3. Uruchom aplikację:

   ```sh
   ./run.sh
   ```

## 🧰 Budowanie pojedynczego pliku (opcjonalne)

Po utworzeniu środowiska:

```sh
./build.sh
```

Wynik dla Linuksa znajdziesz w `dist/Voyager_carton`.

---

> Upewnij się, że masz dostęp do Internetu, aby połączyć się z canisterem ICP.
