"""Nowoczesne GUI do uploadu/pobierania plików z canisterów ICP."""

import asyncio
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from v_file import download_file, list_pins, upload_file

APP_TITLE = "Voyager Carton - ICP File Manager"

# ============ NOWOCZESNA KOLORYSTYKA ============
COLOR_BG = "#0f1419"          # Ciemne tło
COLOR_FRAME = "#1a1f2e"       # Frame / card background
COLOR_ACCENT = "#6366f1"      # Primary color (indigo)
COLOR_ACCENT_DARK = "#4f46e5" # Darker accent
COLOR_SUCCESS = "#10b981"     # Green
COLOR_TEXT = "#e2e8f0"        # Light text
COLOR_TEXT_MUTED = "#94a3b8"  # Muted text
COLOR_BORDER = "#334155"      # Border color


class VoyagerCartonApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("900x1000")
        self.resizable(True, True)
        self.configure(background=COLOR_BG)

        self.canister_id = tk.StringVar()
        self.ic_url = tk.StringVar(value="https://ic0.app")
        self.pin_start = tk.IntVar(value=0)
        self.pin_end = tk.IntVar(value=20)
        self.canister_connected = False
        self.file_index_map = {}

        self._setup_styles()
        self._build_ui()

    def _setup_styles(self):
        """Konfiguruje nowoczesny styl."""
        style = ttk.Style()
        style.theme_use('clam')

        # ===== COLORS =====
        style.configure('TFrame', background=COLOR_BG)
        style.configure('TLabel', background=COLOR_FRAME, foreground=COLOR_TEXT, font=('Segoe UI', 10))
        style.configure('Header.TLabel', background=COLOR_BG, foreground=COLOR_ACCENT, font=('Segoe UI', 16, 'bold'))
        style.configure('Title.TLabel', background=COLOR_FRAME, foreground=COLOR_TEXT, font=('Segoe UI', 12, 'bold'))
        style.configure('TLabelFrame', background=COLOR_FRAME, foreground=COLOR_TEXT, borderwidth=1, relief='solid')
        style.configure('TLabelFrame.Label', background=COLOR_FRAME, foreground=COLOR_ACCENT, font=('Segoe UI', 11, 'bold'))
        
        # ===== ENTRY =====
        style.configure('TEntry', fieldbackground=COLOR_BG, foreground=COLOR_TEXT, borderwidth=1, relief='solid', font=('Segoe UI', 10))
        style.map('TEntry', fieldbackground=[('focus', '#1f2937')])
        
        # ===== BUTTON STYLES =====
        style.configure('Primary.TButton', font=('Segoe UI', 10, 'bold'), padding=10)
        style.map('Primary.TButton',
                  background=[('active', COLOR_ACCENT_DARK), ('pressed', COLOR_ACCENT_DARK)],
                  relief=[('pressed', tk.SUNKEN), ('!pressed', tk.RAISED)])
        
        style.configure('Secondary.TButton', font=('Segoe UI', 10), padding=8)
        style.map('Secondary.TButton',
                  relief=[('pressed', tk.SUNKEN), ('!pressed', tk.RAISED)])

    def _build_ui(self):
        """Buduje interfejs użytkownika."""
        # ========== HEADER ==========
        header = tk.Frame(self, bg=COLOR_BG, highlightthickness=0)
        header.pack(fill='x', padx=0, pady=0)

        header_inner = tk.Frame(header, bg=COLOR_BG, highlightthickness=0)
        header_inner.pack(fill='x', padx=20, pady=20)

        main_title = tk.Label(header_inner, text="📦 Voyager Carton", bg=COLOR_BG, fg=COLOR_ACCENT, font=('Segoe UI', 16, 'bold'))
        main_title.pack(side='left')
        subtitle = tk.Label(header_inner, text="ICP File Manager", bg=COLOR_BG, fg=COLOR_TEXT_MUTED, font=('Segoe UI', 11))
        subtitle.pack(side='left', padx=(10, 0))

        # ========== MAIN CONTAINER ==========
        main_frame = ttk.Frame(self)
        main_frame.pack(fill='both', expand=True, padx=15, pady=15)


        # ========== SECTION 1: CONNECTION ==========
        conn_frame = ttk.LabelFrame(main_frame, text="⚡ Połączenie z Canisterem", padding=15)
        conn_frame.pack(fill='x', pady=(0, 15))

        # Canister ID
        ttk.Label(conn_frame, text="Canister ID:").grid(row=0, column=0, sticky='w', pady=8)
        ttk.Entry(conn_frame, textvariable=self.canister_id, width=45).grid(row=0, column=1, sticky='ew', padx=(10, 0), pady=8)

        # IC URL
        ttk.Label(conn_frame, text="IC URL:").grid(row=1, column=0, sticky='w', pady=8)
        ttk.Entry(conn_frame, textvariable=self.ic_url, width=45).grid(row=1, column=1, sticky='ew', padx=(10, 0), pady=8)

        # Connect button
        connect_btn = ttk.Button(conn_frame, text="🔗 Połącz", command=self.on_connect, style='Primary.TButton')
        connect_btn.grid(row=0, column=2, rowspan=2, padx=(10, 0), sticky='nsew')

        conn_frame.columnconfigure(1, weight=1)

        # ========== SECTION 2: FILES LIST ==========
        list_frame = ttk.LabelFrame(main_frame, text="📁 Lista Dostępnych Plików", padding=15)
        list_frame.pack(fill='both', expand=True, pady=(0, 15))

        # Controls
        control_frame = ttk.Frame(list_frame)
        control_frame.pack(fill='x', pady=(0, 12))

        ttk.Label(control_frame, text="Zakres PIN:", font=('Segoe UI', 10)).pack(side='left', padx=(0, 8))
        ttk.Entry(control_frame, textvariable=self.pin_start, width=5, font=('Segoe UI', 10)).pack(side='left', padx=(0, 8))
        ttk.Label(control_frame, text="→").pack(side='left', padx=(0, 8))
        ttk.Entry(control_frame, textvariable=self.pin_end, width=5, font=('Segoe UI', 10)).pack(side='left', padx=(0, 12))

        ttk.Button(control_frame, text="🔄 Odśwież", command=self.on_refresh_list, style='Primary.TButton').pack(side='left')

        # Files listbox
        listbox_frame = ttk.Frame(list_frame)
        listbox_frame.pack(fill='both', expand=True)

        scrollbar = ttk.Scrollbar(listbox_frame)
        scrollbar.pack(side='right', fill='y')

        self.listbox = tk.Listbox(
            listbox_frame,
            height=6,
            bg=COLOR_BG,
            fg=COLOR_TEXT,
            selectbackground=COLOR_ACCENT,
            activestyle='none',
            relief='flat',
            font=('Segoe UI', 10),
            yscrollcommand=scrollbar.set
        )
        self.listbox.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=self.listbox.yview)

        # Download button
        download_btn = ttk.Button(list_frame, text="📥 Pobierz Wybrany", command=self.on_download_selected, style='Primary.TButton')
        download_btn.pack(fill='x', pady=(12, 0))

        # ========== SECTION 3: UPLOAD ==========
        upload_frame = ttk.LabelFrame(main_frame, text="⬆️ Wgraj Plik", padding=15)
        upload_frame.pack(fill='x', pady=(0, 15))

        self.note_var = tk.StringVar()
        ttk.Label(upload_frame, text="Notatka:").grid(row=0, column=0, sticky='w', pady=8)
        ttk.Entry(upload_frame, textvariable=self.note_var, width=45).grid(row=0, column=1, sticky='ew', padx=(10, 0), pady=8)

        upload_btn = ttk.Button(upload_frame, text="🚀 Wybierz i Wyślij", command=self.on_upload_file, style='Primary.TButton')
        upload_btn.grid(row=0, column=2, padx=(10, 0))

        upload_frame.columnconfigure(1, weight=1)

        # ========== SECTION 4: PROGRESS & STATUS ==========
        status_frame = ttk.Frame(main_frame)
        status_frame.pack(fill='x', pady=(0, 10))

        self.status_label = ttk.Label(status_frame, text="✓ Gotowy", foreground=COLOR_SUCCESS)
        self.status_label.pack(side='left')

        # Progress bar
        progress_container = ttk.Frame(main_frame)
        progress_container.pack(fill='x')

        ttk.Label(progress_container, text="Postęp:").pack(side='left', padx=(0, 8))
        self.progress_var = tk.DoubleVar(value=0)
        self.progress_bar = ttk.Progressbar(progress_container, variable=self.progress_var, maximum=100, mode='determinate', length=300)
        self.progress_bar.pack(side='left', fill='x', expand=True, padx=(0, 12))
        self.progress_label = ttk.Label(progress_container, text="0%", width=5)
        self.progress_label.pack(side='left')

    def _set_status(self, text: str, color=COLOR_TEXT):
        self.status_label.config(text=text, foreground=color)
        self.update_idletasks()

    def _update_progress(self, current: int, total: int):
        if total <= 0:
            return
        progress = (current / total) * 100
        self.progress_var.set(progress)
        self.progress_label.config(text=f"{int(progress)}%")
        self.update_idletasks()

    def _reset_progress(self):
        self.progress_var.set(0)
        self.progress_label.config(text="0%")
        self.update_idletasks()

    def _ensure_connected(self):
        if not self.canister_id.get().strip():
            messagebox.showwarning("Brak canistera", "Podaj ID canistera.")
            return False
        if not self.ic_url.get().strip():
            messagebox.showwarning("Brak URL", "Podaj URL ICP.")
            return False
        self.canister_connected = True
        return True

    def on_connect(self):
        if not self._ensure_connected():
            return
        self._set_status("Połączono. Ładuję listę plików...", COLOR_SUCCESS)
        self.on_refresh_list()

    def on_refresh_list(self):
        if not self._ensure_connected():
            return

        start = self.pin_start.get()
        end = self.pin_end.get()
        if end < start:
            messagebox.showerror("Błąd", "Zakres pin musi być poprawny (end >= start).")
            return

        self._set_status("Pobieranie listy plików...", COLOR_ACCENT)
        self.listbox.delete(0, tk.END)
        self.file_index_map.clear()

        try:
            pins = asyncio.run(list_pins(self.canister_id.get().strip(), start, end, ic_url=self.ic_url.get().strip()))
        except Exception as e:
            messagebox.showerror("Błąd", f"Nie udało się pobrać listy: {e}")
            self._set_status("Błąd pobierania listy.", COLOR_TEXT)
            return

        for idx, entry in enumerate(pins):
            if entry.get("error"):
                display = f"⚠️  [{entry['index']}] <ERROR>"
            else:
                display = f"📄 [{entry['index']}] {entry['name']}"
            self.listbox.insert(tk.END, display)
            self.file_index_map[idx] = {"pin": entry["index"], "name": entry.get("name"), "error": entry.get("error", False)}

        self._set_status(f"✓ Załadowano {len(pins)} plików", COLOR_SUCCESS)

    def on_download_selected(self):
        if not self._ensure_connected():
            return

        selection = self.listbox.curselection()
        if not selection:
            messagebox.showinfo("Brak wyboru", "Wybierz plik z listy.")
            return

        idx = selection[0]
        entry = self.file_index_map.get(idx)
        if not entry or entry.get("error"):
            messagebox.showwarning("Błąd", "Plik nie istnieje lub nie można go odczytać.")
            return

        pin_idx = entry["pin"]
        file_name = entry.get("name") or "plik"

        save_path = filedialog.asksaveasfilename(title="Zapisz jako", initialfile=file_name, filetypes=[("Wszystkie pliki", "*")])
        if not save_path:
            return

        self._reset_progress()
        self._set_status(f"Pobieram plik (pin {pin_idx})...", COLOR_ACCENT)
        try:
            saved_path = asyncio.run(download_file(self.canister_id.get().strip(), pin_idx, save_path=save_path, ic_url=self.ic_url.get().strip(), progress_callback=self._update_progress))
        except Exception as e:
            messagebox.showerror("Błąd pobierania", str(e))
            self._set_status("Błąd pobierania.", COLOR_TEXT)
            self._reset_progress()
            return

        if saved_path:
            messagebox.showinfo("Sukces", f"Plik zapisano: {saved_path}")
            self._set_status(f"✓ Plik pobrany: {os.path.basename(saved_path)}", COLOR_SUCCESS)
        else:
            self._set_status("Nie udało się pobrać pliku.", COLOR_TEXT)
        self._reset_progress()

    def on_upload_file(self):
        if not self._ensure_connected():
            return

        file_path = filedialog.askopenfilename(title="Wybierz plik do wgrania")
        if not file_path:
            return

        note = self.note_var.get().strip()
        self._reset_progress()
        self._set_status("Wysyłam plik do canistera...", COLOR_ACCENT)

        try:
            result = asyncio.run(upload_file(self.canister_id.get().strip(), file_path, note, ic_url=self.ic_url.get().strip(), progress_callback=self._update_progress))
        except Exception as e:
            messagebox.showerror("Błąd wysyłania", str(e))
            self._set_status("Błąd wysyłania.", COLOR_TEXT)
            self._reset_progress()
            return

        if result and result.get("pin_index") is not None:
            messagebox.showinfo("Sukces", f"Wgrano plik. Pin index: {result['pin_index']}\nRozmiar: {result['size_MB']} MB")
            self._set_status(f"✓ Plik wgrany (pin={result['pin_index']})", COLOR_SUCCESS)
            self.on_refresh_list()
        else:
            self._set_status("Wgrywanie zakończone niepowodzeniem.", COLOR_TEXT)
        self._reset_progress()


if __name__ == "__main__":
    app = VoyagerCartonApp()
    app.mainloop()
