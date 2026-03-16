"""Prosty GUI do uploadu/pobierania plików z canisterów ICP."""

import asyncio
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from v_file import download_file, list_pins, upload_file

APP_TITLE = "Voyager Carton - ICP File Manager"

# Stylizacja dla ciemnego motywu
DARK_BG = "#1f2024"
DARK_FRAME = "#25272d"
DARK_FG = "#e8e8e8"
DARK_ENTRY = "#2f3137"


class VoyagerCartonApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("1700x1000")
        self.resizable(False, False)

        self.canister_id = tk.StringVar()
        self.ic_url = tk.StringVar(value="https://ic0.app")
        self.pin_start = tk.IntVar(value=0)
        self.pin_end = tk.IntVar(value=20)
        self.canister_connected = False
        self.file_index_map = {}  # listbox index -> pin index

        self._apply_dark_theme()
        self._build_ui()

    def _apply_dark_theme(self):
        style = ttk.Style(self)
        style.theme_use("clam")

        style.configure("TLabel", background=DARK_FRAME, foreground=DARK_FG)
        style.configure("TLabelFrame", background=DARK_FRAME, foreground=DARK_FG)
        style.configure("TEntry", fieldbackground=DARK_ENTRY, foreground=DARK_FG)
        style.configure("TButton", background=DARK_FRAME, foreground=DARK_FG)
        style.configure("TFrame", background=DARK_BG)
        self.configure(background=DARK_BG)

    def _build_ui(self):
        frame = ttk.Frame(self)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Canister connection
        conn_frame = ttk.LabelFrame(frame, text="Połączenie z canisterem")
        conn_frame.pack(fill="x", padx=0, pady=6)

        ttk.Label(conn_frame, text="Canister ID:").grid(row=0, column=0, sticky="w")
        ttk.Entry(conn_frame, textvariable=self.canister_id, width=52).grid(
            row=0, column=1, sticky="w", padx=4
        )
        ttk.Button(conn_frame, text="Połącz", command=self.on_connect).grid(row=0, column=2, padx=4)

        ttk.Label(conn_frame, text="IC URL:").grid(row=1, column=0, sticky="w", pady=(6, 0))
        ttk.Entry(conn_frame, textvariable=self.ic_url, width=52).grid(
            row=1, column=1, sticky="w", padx=4, pady=(6, 0)
        )

        # File list
        list_frame = ttk.LabelFrame(frame, text="Lista dostępnych plików (piny)")
        list_frame.pack(fill="both", expand=True, padx=0, pady=6)

        tools_frame = ttk.Frame(list_frame)
        tools_frame.pack(fill="x", pady=(0, 6))

        ttk.Label(tools_frame, text="Zakres pin: od").pack(side="left")
        ttk.Entry(tools_frame, width=6, textvariable=self.pin_start).pack(side="left", padx=(4, 8))
        ttk.Label(tools_frame, text="do").pack(side="left")
        ttk.Entry(tools_frame, width=6, textvariable=self.pin_end).pack(side="left", padx=(4, 8))
        ttk.Button(tools_frame, text="Odśwież listę", command=self.on_refresh_list).pack(side="left", padx=4)
        ttk.Button(tools_frame, text="Pobierz wybrany", command=self.on_download_selected).pack(
            side="right", padx=4
        )

        self.listbox = tk.Listbox(list_frame, height=16, bg=DARK_ENTRY, fg=DARK_FG, selectbackground="#3b4b65")
        self.listbox.pack(fill="both", expand=True)

        # Upload
        upload_frame = ttk.LabelFrame(frame, text="Wgraj plik")
        upload_frame.pack(fill="x", padx=0, pady=6)

        self.note_var = tk.StringVar()
        ttk.Label(upload_frame, text="Notatka:").grid(row=0, column=0, sticky="w")
        ttk.Entry(upload_frame, textvariable=self.note_var, width=60).grid(
            row=0, column=1, sticky="w", padx=4
        )
        ttk.Button(upload_frame, text="Wybierz plik i wgraj", command=self.on_upload_file).grid(
            row=0, column=2, padx=4
        )

        status_frame = ttk.Frame(frame)
        status_frame.pack(fill="x", pady=(10, 0))
        self.status_label = ttk.Label(status_frame, text="Gotowy.")
        self.status_label.pack(side="left")

    def _set_status(self, text: str):
        self.status_label.config(text=text)
        self.update_idletasks()

    def _ensure_connected(self):
        if not self.canister_id.get().strip():
            messagebox.showwarning("Brak canistera", "Podaj ID canistera.")
            return False
        if not self.ic_url.get().strip():
            messagebox.showwarning("Brak URL", "Podaj URL ICP (np. https://ic0.app).")
            return False
        self.canister_connected = True
        return True

    def on_connect(self):
        if not self._ensure_connected():
            return
        self._set_status("Połączono. Załaduj listę plików.")
        self.on_refresh_list()

    def on_refresh_list(self):
        if not self._ensure_connected():
            return

        start = self.pin_start.get()
        end = self.pin_end.get()
        if end < start:
            messagebox.showerror("Błąd", "Zakres pin musi być poprawny (end >= start).")
            return

        self._set_status("Pobieranie listy plików...")
        self.listbox.delete(0, tk.END)
        self.file_index_map.clear()

        try:
            pins = asyncio.run(
                list_pins(
                    self.canister_id.get().strip(),
                    start,
                    end,
                    ic_url=self.ic_url.get().strip(),
                )
            )
        except Exception as e:
            messagebox.showerror("Błąd", f"Nie udało się pobrać listy: {e}")
            self._set_status("Błąd pobierania listy.")
            return

        for idx, entry in enumerate(pins):
            if entry.get("error"):
                display = f"[{entry['index']}] <ERROR>"
            else:
                display = f"[{entry['index']}] {entry['name']}"
            self.listbox.insert(tk.END, display)
            self.file_index_map[idx] = {"pin": entry["index"], "name": entry.get("name"), "error": entry.get("error", False)}

        self._set_status(f"Znaleziono {len(pins)} plików.")

    def on_download_selected(self):
        if not self._ensure_connected():
            return

        selection = self.listbox.curselection()
        if not selection:
            messagebox.showinfo("Brak wyboru", "Wybierz plik z listy.")
            return

        idx = selection[0]
        entry = self.file_index_map.get(idx)
        if not entry:
            messagebox.showerror("Błąd", "Nie udało się znaleźć indeksu pliku.")
            return

        pin_idx = entry["pin"]
        file_name = entry.get("name") or "plik"

        # Jeśli w liście znalazło się <ERROR>, zatrzymujemy pobieranie
        if entry.get("error"):
            messagebox.showwarning("Błąd", "Wybrany plik nie istnieje lub nie można go odczytać.")
            return

        # Pytamy użytkownika, gdzie zapisać
        save_path = filedialog.asksaveasfilename(
            title="Zapisz jako",
            initialfile=file_name,
            defaultextension="",
            filetypes=[("Wszystkie pliki", "*")],
        )
        if not save_path:
            return

        self._set_status(f"Pobieram plik (pin {pin_idx})...")
        try:
            saved_path = asyncio.run(
                download_file(
                    self.canister_id.get().strip(),
                    pin_idx,
                    save_path=save_path,
                    ic_url=self.ic_url.get().strip(),
                )
            )
        except Exception as e:
            messagebox.showerror("Błąd pobierania", str(e))
            self._set_status("Błąd pobierania.")
            return

        if saved_path:
            messagebox.showinfo("Sukces", f"Plik zapisano: {saved_path}")
            self._set_status(f"Plik pobrany: {saved_path}")
        else:
            self._set_status("Nie udało się pobrać pliku.")

    def on_upload_file(self):
        if not self._ensure_connected():
            return

        file_path = filedialog.askopenfilename(title="Wybierz plik do wgrania")
        if not file_path:
            return

        note = self.note_var.get().strip()
        self._set_status("Wysyłam plik do canistera...")

        try:
            result = asyncio.run(
                upload_file(
                    self.canister_id.get().strip(),
                    file_path,
                    note,
                    ic_url=self.ic_url.get().strip(),
                )
            )
        except Exception as e:
            messagebox.showerror("Błąd wysyłania", str(e))
            self._set_status("Błąd wysyłania.")
            return

        if result and result.get("pin_index") is not None:
            messagebox.showinfo(
                "Sukces",
                f"Wgrano plik. Pin index: {result['pin_index']}\nRozmiar: {result['size_MB']} MB",
            )
            self._set_status(f"Plik wgrany (pin={result['pin_index']}).")
            self.on_refresh_list()
        else:
            self._set_status("Wgrywanie zakończone niepowodzeniem.")


if __name__ == "__main__":
    app = VoyagerCartonApp()
    app.mainloop()
