import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import customtkinter as ctk

# ==========================================================
# CONVERSIÓN PNG / JPG ↔ WEBP
# ==========================================================
def convertir_png_webp(entradas, carpeta_salida, modo, calidad=85):
    if not os.path.exists(carpeta_salida):
        os.makedirs(carpeta_salida)

    for ruta_entrada in entradas:
        if os.path.isdir(ruta_entrada):
            continue

        nombre_archivo = os.path.basename(ruta_entrada)
        ext = nombre_archivo.lower()

        try:
            # --- PNG o JPG → WEBP ---
            if modo == "PNG/JPG → WEBP" and (ext.endswith(".png") or ext.endswith(".jpg") or ext.endswith(".jpeg")):
                nombre = os.path.splitext(nombre_archivo)[0]
                salida = os.path.join(carpeta_salida, nombre + ".webp")
                Image.open(ruta_entrada).save(salida, "webp", quality=calidad)

            # --- WEBP → PNG ---
            elif modo == "WEBP → PNG":
                nombre = os.path.splitext(nombre_archivo)[0]
                salida = os.path.join(carpeta_salida, nombre + ".png")
                Image.open(ruta_entrada).save(salida, "png")

            print(f"✅ {nombre_archivo} → {os.path.basename(salida)}")

        except Exception as e:
            print(f"⚠️ Error con {nombre_archivo}: {e}")


# ==========================================================
# INTERFAZ ATENEA
# ==========================================================
class AteneaApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Atenea Convert PNG/JPG ↔ WEBP")
        self.geometry("600x510")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # --- ICONO ---
        icon_ico = self.resource("logo.ico")
        icon_png = self.resource("logo.png")

        if os.path.exists(icon_png):
            try:
                img = tk.PhotoImage(file=icon_png)
                self.iconphoto(True, img)
            except:
                pass

        if os.path.exists(icon_ico):
            try:
                self.iconbitmap(icon_ico)
            except:
                pass

        # --- TÍTULO ---
        self.label_title = ctk.CTkLabel(self, text="Atenea Convert PNG/JPG ↔ WEBP",
                                        font=("Segoe UI", 21, "bold"), text_color="#2196F3")
        self.label_title.pack(pady=20)

        # --- INPUT ---
        self.label_in = ctk.CTkLabel(self, text="📂 Input folder or images:", font=("Segoe UI", 14))
        self.label_in.pack()
        self.entry_in = ctk.CTkEntry(self, width=400)
        self.entry_in.insert(0, "")
        self.entry_in.pack(pady=5)
        self.btn_in = ctk.CTkButton(self, text="Select files/folder", command=self.select_in)
        self.btn_in.pack(pady=5)

        # --- OUTPUT ---
        self.label_out = ctk.CTkLabel(self, text="📁 Output folder:", font=("Segoe UI", 14))
        self.label_out.pack(pady=(12, 0))
        self.entry_out = ctk.CTkEntry(self, width=400)
        self.entry_out.insert(0, "convert")
        self.entry_out.pack(pady=5)
        self.btn_out = ctk.CTkButton(self, text="Select folder", command=self.select_out)
        self.btn_out.pack(pady=5)

        # --- FORMAT OPTION ---
        self.label_fmt = ctk.CTkLabel(self, text="🎨 Conversion mode:", font=("Segoe UI", 14))
        self.label_fmt.pack(pady=(18, 5))
        self.formato = ctk.CTkOptionMenu(self, values=["PNG/JPG → WEBP", "WEBP → PNG"])
        self.formato.pack()

        # --- CONVERT BUTTON ---
        self.btn_convert = ctk.CTkButton(self, text="Convert", font=("Segoe UI", 16, "bold"),
                                         fg_color="#2196F3", hover_color="#1976D2",
                                         width=170, height=45, command=self.convert)
        self.btn_convert.pack(pady=30)

        # --- FOOTER ---
        self.footer = ctk.CTkLabel(self, text="© 2025 Atenea Store Tools", text_color="#2196F3",
                                   font=("Segoe UI", 10))
        self.footer.pack(side="bottom", pady=10)

        self.selected_files = []  # 🔹 Guardará las rutas si el usuario elige archivos sueltos

    def select_in(self):
        choice = messagebox.askyesno(
            "Select files or folder",
            "Do you want to select specific images?\n(Yes = select images, No = select folder)"
        )
        if choice:
            files = filedialog.askopenfilenames(
                title="Select images",
                filetypes=[
                    ("Images", "*.png *.jpg *.jpeg *.webp"),
                    ("All files", "*.*")
                ]
            )
            if files:
                self.selected_files = list(files)
                self.entry_in.delete(0, tk.END)
                self.entry_in.insert(0, f"{len(files)} files selected")
        else:
            folder = filedialog.askdirectory()
            if folder:
                self.selected_files = []
                self.entry_in.delete(0, tk.END)
                self.entry_in.insert(0, folder)

    def select_out(self):
        folder = filedialog.askdirectory()
        if folder:
            self.entry_out.delete(0, tk.END)
            self.entry_out.insert(0, folder)

    def convert(self):
        carpeta_salida = self.entry_out.get().strip()
        modo = self.formato.get()

        if not carpeta_salida:
            messagebox.showerror("Error", "Debe seleccionar una carpeta de salida.")
            return

        # Determinar si el usuario seleccionó archivos o carpeta
        if self.selected_files:
            entradas = self.selected_files
        else:
            carpeta_entrada = self.entry_in.get().strip()
            if not carpeta_entrada:
                messagebox.showerror("Error", "Debe seleccionar una carpeta o archivos.")
                return
            entradas = [os.path.join(carpeta_entrada, f) for f in os.listdir(carpeta_entrada)
                        if f.lower().endswith((".png", ".jpg", ".jpeg", ".webp"))]

        try:
            convertir_png_webp(entradas, carpeta_salida, modo)
            messagebox.showinfo("Completado", "✅ ¡Conversión finalizada!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def resource(self, path):
        try:
            base = sys._MEIPASS
        except:
            base = os.path.abspath(".")
        return os.path.join(base, path)


# ==========================================================
# EJECUCIÓN
# ==========================================================
if __name__ == "__main__":
    app = AteneaApp()
    app.mainloop()
