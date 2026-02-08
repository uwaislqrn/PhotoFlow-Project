import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import re

class PhotoFlowApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PhotoFlow - Professional Graduation Photographer Workflow")
        
        # --- KONFIGURASI TEMA ---
        self.bg_color = "#2e2e2e"
        self.fg_color = "#ffffff"
        self.entry_bg = "#444444"
        self.button_color = "#555555"
        self.success_color = "#00FF00" 
        self.move_color = "#2196F3"
        self.footer_color = "#00FF00"
        self.disabled_color = "#777777"
        self.root.configure(bg=self.bg_color)

        # --- LOGIKA MUNCUL DI TENGAH LAYAR ---
        app_width = 600
        app_height = 850
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width // 2) - (app_width // 2)
        y = (screen_height // 2) - (app_height // 2)
        self.root.geometry(f"{app_width}x{app_height}+{x}+{y}")

        try:
            # Pastikan logo.ico ada di folder yang sama saat menjalankan script
            self.root.iconbitmap("logo.ico") 
        except:
            pass

        # --- VARIABEL STATE ---
        self.source_f1 = tk.StringVar(); self.target_f1 = tk.StringVar()
        self.copy_mode_f1 = tk.StringVar(value="Hanya RAW")
        self.raw_type_f1 = tk.StringVar(value=".ARW (Sony)")

        self.source_f2 = tk.StringVar(); self.target_f2 = tk.StringVar()

        self.rename_mode_f3 = tk.StringVar(value="RAW + JPG")
        self.raw_folder_f3 = tk.StringVar(); self.jpg_folder_f3 = tk.StringVar()
        self.client_name_f3 = tk.StringVar()

        self.raw_options = [".ARW (Sony)", ".CR2 (Canon)", ".CR3 (Canon New)", ".NEF (Nikon)", ".RAF (Fujifilm)", ".RW2 (Lumix)", ".ORF (Olympus)", ".DNG (Adobe/Pentax)"]

        self.setup_ui()

    def open_folder(self, path):
        """Membuka folder di Windows Explorer"""
        if path and os.path.exists(path):
            os.startfile(path)
        else:
            messagebox.showwarning("Peringatan", "Folder tidak ditemukan atau belum dipilih.")

    def clear_log(self, log_widget):
        """Menghapus isi log"""
        log_widget.delete("1.0", tk.END)

    def setup_ui(self):
        nav_frame = tk.Frame(self.root, bg=self.bg_color); nav_frame.pack(pady=10)
        btn_s = {"bg": self.button_color, "fg": self.fg_color, "width": 18, "font": ("Arial", 10, "bold")}
        tk.Button(nav_frame, text="1. File Copy", command=self.show_f1, **btn_s).pack(side="left", padx=5)
        tk.Button(nav_frame, text="2. Memory Card Copy", command=self.show_f2, **btn_s).pack(side="left", padx=5)
        tk.Button(nav_frame, text="3. Rename File", command=self.show_f3, **btn_s).pack(side="left", padx=5)

        self.main_container = tk.Frame(self.root, bg=self.bg_color)
        self.main_container.pack(fill="both", expand=True)

        self.create_tab1(); self.create_tab2(); self.create_tab3()
        
        footer = tk.Label(self.root, text="© 2025 PhotoFlow - Workflow Optimization by Uwais Al Qarni - IG @uwaislqrn", 
                          bg=self.bg_color, fg=self.footer_color, font=("Arial", 8, "italic"))
        footer.pack(side="bottom", pady=10)
        self.show_f1()

    def toggle_f1_visual(self, e=None):
        is_jpg = self.copy_mode_f1.get() == "Hanya JPG"
        self.raw_drop_f1.config(state="disabled" if is_jpg else "readonly")
        self.raw_lab_f1.config(fg=self.disabled_color if is_jpg else self.fg_color)

    def toggle_f3_visual(self, e=None):
        m = self.rename_mode_f3.get()
        r_s = "normal" if m != "Hanya JPG" else "disabled"
        self.raw_lab_f3.config(fg=self.fg_color if r_s == "normal" else self.disabled_color)
        self.raw_ent_f3.config(state=r_s, disabledbackground=self.bg_color) 
        self.raw_btn_f3.config(state=r_s)
        j_s = "normal" if m != "Hanya RAW" else "disabled"
        self.jpg_lab_f3.config(fg=self.fg_color if j_s == "normal" else self.disabled_color)
        self.jpg_ent_f3.config(state=j_s, disabledbackground=self.bg_color)
        self.jpg_btn_f3.config(state=j_s)

    def create_tab1(self):
        self.tab1 = tk.Frame(self.main_container, bg=self.bg_color)
        tk.Label(self.tab1, text="RAW & JPG FILE COPY (LIST)", font=("Arial", 16, "bold"), bg=self.bg_color, fg=self.fg_color).pack(pady=10)
        f = tk.Frame(self.tab1, bg=self.bg_color); f.pack(fill="x", padx=20)
        
        tk.Label(f, text="Folder Asal:", bg=self.bg_color, fg=self.fg_color, width=15, anchor="w").grid(row=0, column=0)
        tk.Entry(f, textvariable=self.source_f1, width=60, bg=self.entry_bg, fg=self.fg_color, insertbackground="white").grid(row=0, column=1, padx=10)
        tk.Button(f, text="Browse", command=lambda: self.source_f1.set(filedialog.askdirectory())).grid(row=0, column=2)
        
        tk.Label(f, text="Folder Tujuan:", bg=self.bg_color, fg=self.fg_color, width=15, anchor="w").grid(row=1, column=0, pady=5)
        tk.Entry(f, textvariable=self.target_f1, width=60, bg=self.entry_bg, fg=self.fg_color, insertbackground="white").grid(row=1, column=1, padx=10)
        tk.Button(f, text="Browse", command=lambda: self.target_f1.set(filedialog.askdirectory())).grid(row=1, column=2)
        
        tk.Label(f, text="Mode Copy:", bg=self.bg_color, fg=self.fg_color, width=15, anchor="w").grid(row=2, column=0)
        cb = ttk.Combobox(f, textvariable=self.copy_mode_f1, values=["Hanya RAW", "Hanya JPG"], state="readonly", width=57)
        cb.grid(row=2, column=1, sticky="w", padx=10, pady=5); cb.bind("<<ComboboxSelected>>", self.toggle_f1_visual)
        
        self.raw_lab_f1 = tk.Label(f, text="Tipe RAW:", bg=self.bg_color, fg=self.fg_color, width=15, anchor="w")
        self.raw_lab_f1.grid(row=3, column=0)
        self.raw_drop_f1 = ttk.Combobox(f, textvariable=self.raw_type_f1, values=self.raw_options, state="readonly", width=57)
        self.raw_drop_f1.grid(row=3, column=1, sticky="w", padx=10)

        tk.Label(self.tab1, text="List Kode File:", bg=self.bg_color, fg=self.fg_color).pack(anchor="w", padx=20, pady=5)
        self.txt1 = tk.Text(self.tab1, height=8, bg=self.entry_bg, fg=self.fg_color, insertbackground="white"); self.txt1.pack(padx=20, fill="both")
        
        btn_f = tk.Frame(self.tab1, bg=self.bg_color); btn_f.pack(pady=10)
        tk.Button(btn_f, text="🚀 Copy", command=lambda: self.process_tab1(False), bg="#4CAF50", fg=self.fg_color, width=15).grid(row=0, column=0, padx=5)
        tk.Button(btn_f, text="🌊 Pindah", command=lambda: self.process_tab1(True), bg=self.move_color, fg=self.fg_color, width=15).grid(row=0, column=1, padx=5)
        tk.Button(btn_f, text="📂 Buka Tujuan", command=lambda: self.open_folder(self.target_f1.get()), bg=self.button_color, fg=self.fg_color, width=15).grid(row=0, column=2, padx=5)
        tk.Button(btn_f, text="🧹 Hapus Log", command=lambda: self.clear_log(self.log1), bg=self.button_color, fg=self.fg_color, width=15).grid(row=0, column=3, padx=5)

        self.log1 = tk.Text(self.tab1, height=10, bg=self.entry_bg, fg=self.fg_color)
        self.log1.tag_config("success", foreground="#00FF00") 
        self.log1.tag_config("fail", foreground="#FF5252") 
        self.log1.pack(padx=20, fill="both", expand=True)

    def create_tab2(self):
        self.tab2 = tk.Frame(self.main_container, bg=self.bg_color)
        tk.Label(self.tab2, text="MEMORY CARD GROUPING", font=("Arial", 16, "bold"), bg=self.bg_color, fg=self.fg_color).pack(pady=10)
        f = tk.Frame(self.tab2, bg=self.bg_color); f.pack(fill="x", padx=20)
        tk.Label(f, text="Folder SD Card:", bg=self.bg_color, fg=self.fg_color, width=15, anchor="w").grid(row=0, column=0)
        tk.Entry(f, textvariable=self.source_f2, width=60, bg=self.entry_bg, fg=self.fg_color).grid(row=0, column=1, padx=10)
        tk.Button(f, text="Browse", command=lambda: self.source_f2.set(filedialog.askdirectory())).grid(row=0, column=2)
        tk.Label(f, text="Folder Tujuan:", bg=self.bg_color, fg=self.fg_color, width=15, anchor="w").grid(row=1, column=0, pady=5)
        tk.Entry(f, textvariable=self.target_f2, width=60, bg=self.entry_bg, fg=self.fg_color).grid(row=1, column=1, padx=10)
        tk.Button(f, text="Browse", command=lambda: self.target_f2.set(filedialog.askdirectory())).grid(row=1, column=2)
        
        btn_f2 = tk.Frame(self.tab2, bg=self.bg_color); btn_f2.pack(pady=20)
        tk.Button(btn_f2, text="🚀 Grouping", command=self.process_tab2, bg="#4CAF50", fg=self.fg_color, width=15).grid(row=0, column=0, padx=5)
        tk.Button(btn_f2, text="📂 Buka Tujuan", command=lambda: self.open_folder(self.target_f2.get()), bg=self.button_color, fg=self.fg_color, width=15).grid(row=0, column=1, padx=5)
        tk.Button(btn_f2, text="🧹 Hapus Log", command=lambda: self.clear_log(self.log2), bg=self.button_color, fg=self.fg_color, width=15).grid(row=0, column=2, padx=5)

        self.log2 = tk.Text(self.tab2, height=15, bg=self.entry_bg, fg=self.fg_color); self.log2.pack(padx=20, fill="both", expand=True)

    def create_tab3(self):
        self.tab3 = tk.Frame(self.main_container, bg=self.bg_color)
        tk.Label(self.tab3, text="RENAME FILE", font=("Arial", 16, "bold"), bg=self.bg_color, fg=self.fg_color).pack(pady=10)
        f = tk.Frame(self.tab3, bg=self.bg_color); f.pack(fill="x", padx=20)
        tk.Label(f, text="Mode Rename:", bg=self.bg_color, fg=self.fg_color, width=15, anchor="w").grid(row=0, column=0)
        cb = ttk.Combobox(f, textvariable=self.rename_mode_f3, values=["RAW + JPG", "Hanya RAW", "Hanya JPG"], state="readonly", width=57)
        cb.grid(row=0, column=1, sticky="w", padx=10, pady=5); cb.bind("<<ComboboxSelected>>", self.toggle_f3_visual)
        self.raw_lab_f3 = tk.Label(f, text="Folder RAW:", bg=self.bg_color, fg=self.fg_color, width=15, anchor="w"); self.raw_lab_f3.grid(row=1, column=0)
        self.raw_ent_f3 = tk.Entry(f, textvariable=self.raw_folder_f3, width=60, bg=self.entry_bg, fg=self.fg_color, insertbackground="white"); self.raw_ent_f3.grid(row=1, column=1, padx=10)
        self.raw_btn_f3 = tk.Button(f, text="Browse", command=lambda: self.raw_folder_f3.set(filedialog.askdirectory())); self.raw_btn_f3.grid(row=1, column=2)
        self.jpg_lab_f3 = tk.Label(f, text="Folder JPG:", bg=self.bg_color, fg=self.fg_color, width=15, anchor="w"); self.jpg_lab_f3.grid(row=2, column=0, pady=5)
        self.jpg_ent_f3 = tk.Entry(f, textvariable=self.jpg_folder_f3, width=60, bg=self.entry_bg, fg=self.fg_color, insertbackground="white"); self.jpg_ent_f3.grid(row=2, column=1, padx=10)
        self.jpg_btn_f3 = tk.Button(f, text="Browse", command=lambda: self.jpg_folder_f3.set(filedialog.askdirectory())); self.jpg_btn_f3.grid(row=2, column=2)
        tk.Label(f, text="Nama Klien:", bg=self.bg_color, fg=self.fg_color, width=15, anchor="w").grid(row=3, column=0)
        tk.Entry(f, textvariable=self.client_name_f3, width=60, bg=self.entry_bg, fg=self.fg_color, insertbackground="white").grid(row=3, column=1, padx=10, pady=10)
        
        btn_f3 = tk.Frame(self.tab3, bg=self.bg_color); btn_f3.pack(pady=10)
        tk.Button(btn_f3, text="✏️ Eksekusi Rename", command=self.process_tab3, bg=self.move_color, fg=self.fg_color, width=20).grid(row=0, column=0, padx=5)
        tk.Button(btn_f3, text="📂 Buka RAW", command=lambda: self.open_folder(self.raw_folder_f3.get()), bg=self.button_color, fg=self.fg_color, width=12).grid(row=0, column=1, padx=5)
        tk.Button(btn_f3, text="📂 Buka JPG", command=lambda: self.open_folder(self.jpg_folder_f3.get()), bg=self.button_color, fg=self.fg_color, width=12).grid(row=0, column=2, padx=5)
        tk.Button(btn_f3, text="🧹 Hapus Log", command=lambda: self.clear_log(self.log3), bg=self.button_color, fg=self.fg_color, width=12).grid(row=0, column=3, padx=5)

        self.log3 = tk.Text(self.tab3, height=15, bg=self.entry_bg, fg=self.fg_color)
        self.log3.tag_config("success", foreground="#00FF00")
        self.log3.tag_config("fail", foreground="#FF5252")
        self.log3.pack(padx=20, fill="both", expand=True)

    # --- LOGIKA PROSES ---
    def process_tab1(self, is_move):
        src, dst, mode = self.source_f1.get(), self.target_f1.get(), self.copy_mode_f1.get()
        if not src or not dst: return
        raw_ext = self.raw_type_f1.get().split(" ")[0].upper()
        raw_input = self.txt1.get("1.0", tk.END)
        codes = [c.strip() for c in re.split(r'[,\n\r\s]+', raw_input) if c.strip()]
        self.log1.delete("1.0", tk.END)
        all_files = os.listdir(src)
        for c in codes:
            found_count = 0
            clean_c = re.sub(r'^(\d+[\.\)]|\-)', '', c).strip()
            base_code = os.path.splitext(clean_c)[0].upper()
            patterns = [re.compile(f".*{re.escape(base_code)}.*", re.IGNORECASE)]
            if base_code.isdigit():
                numeric_c = str(int(base_code))
                patterns.append(re.compile(f".*\\s*{re.escape(numeric_c)}$", re.IGNORECASE))
                patterns.append(re.compile(f".*\\(\\s*{re.escape(numeric_c)}\\s*\\)", re.IGNORECASE))
            for filename in all_files:
                name, ext = os.path.splitext(filename); ext = ext.upper(); is_r, is_j = (ext == raw_ext), (ext in [".JPG", ".JPEG"])
                if not ((mode == "Hanya RAW" and is_r) or (mode == "Hanya JPG" and is_j)): continue
                if any(p.search(name) for p in patterns):
                    try:
                        (shutil.move if is_move else shutil.copy2)(os.path.join(src, filename), os.path.join(dst, filename))
                        self.log1.insert(tk.END, f"✔️ Berhasil: {filename}\n", "success")
                        found_count += 1
                    except:
                        self.log1.insert(tk.END, f"❌ Gagal: {filename} (File terkunci)\n", "fail")
            if found_count == 0: self.log1.insert(tk.END, f"⚠️ Tidak Ditemukan: {c}\n", "fail")
        self.log1.see(tk.END); messagebox.showinfo("Selesai", "Proses Selesai!")

    def process_tab2(self):
        src, dst = self.source_f2.get(), self.target_f2.get()
        if not src or not dst: return
        os.makedirs(os.path.join(dst, "JPG"), exist_ok=True); os.makedirs(os.path.join(dst, "RAW"), exist_ok=True)
        self.log2.delete("1.0", tk.END)
        for f in os.listdir(src):
            ext = os.path.splitext(f)[1].upper()
            sub = "JPG" if ext in [".JPG", ".JPEG"] else "RAW" if any(r in ext for r in [".ARW",".CR2",".CR3",".NEF",".RAF",".RW2",".ORF",".DNG",".PEF"]) else None
            if sub:
                try:
                    shutil.copy2(os.path.join(src, f), os.path.join(dst, sub, f))
                    self.log2.insert(tk.END, f"✔️ {sub}: {f}\n")
                except:
                    self.log2.insert(tk.END, f"❌ Gagal: {f}\n")
        messagebox.showinfo("Selesai", "Grouping Selesai!")

    def process_tab3(self):
        mode, name = self.rename_mode_f3.get(), self.client_name_f3.get().strip()
        if not name: return
        self.log3.delete("1.0", tk.END)
        def get_sort_key(filename):
            match = re.search(r'(\d+)', os.path.splitext(filename)[0])
            return int(match.group(1)) if match else filename.lower()
        tasks = []
        if mode != "Hanya JPG": tasks.append((self.raw_folder_f3.get(), "RAW"))
        if mode != "Hanya RAW": tasks.append((self.jpg_folder_f3.get(), "JPG"))
        for folder, label in tasks:
            if not folder or not os.path.exists(folder): continue
            files = sorted([f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))], key=get_sort_key)
            for i, f in enumerate(files, 1):
                ext = os.path.splitext(f)[1]
                try:
                    os.rename(os.path.join(folder, f), os.path.join(folder, f"{name} ({i}){ext}"))
                    self.log3.insert(tk.END, f"✔️ {label}: {f} -> {name} ({i}){ext}\n", "success")
                except:
                    self.log3.insert(tk.END, f"❌ Gagal: {f} (Sedang dibuka)\n", "fail")
        messagebox.showinfo("Selesai", "Rename Berhasil!")

    def show_f1(self): [f.pack_forget() for f in [self.tab1, self.tab2, self.tab3]]; self.tab1.pack(fill="both", expand=True)
    def show_f2(self): [f.pack_forget() for f in [self.tab1, self.tab2, self.tab3]]; self.tab2.pack(fill="both", expand=True)
    def show_f3(self): [f.pack_forget() for f in [self.tab1, self.tab2, self.tab3]]; self.tab3.pack(fill="both", expand=True)

if __name__ == "__main__":
    root = tk.Tk(); app = PhotoFlowApp(root); root.mainloop()