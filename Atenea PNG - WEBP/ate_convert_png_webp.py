import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import customtkinter as ctk

# ==========================================================
# CONVERSIÓN PNG ↔ WEBP
# ==========================================================
def convertir_png_webp(carpeta_entrada, carpeta_salida, modo, calidad=85):
    if not os.path.exists(carpeta_salida):
        os.makedirs(carpeta_salida)

    for nombre_archivo in os.listdir(carpeta_entrada):
        ruta_entrada = os.path.join(carpeta_entrada, nombre_archivo)

        if os.path.isdir(ruta_entrada):
            continue

        ext = nombre_archivo.lower()

        try:
            if modo == "PNG → WEBP" and ext.endswith(".png"):
                nombre = os.path.splitext(nombre_archivo)[0]
                salida = os.path.join(carpeta_salida, nombre + ".webp")
                Image.open(ruta_entrada).save(salida, "webp", quality=calidad)

            elif modo == "WEBP → PNG" and ext.endswith(".webp"):
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
        self.title("Atenea Convert PNG ↔ WEBP")
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
        self.label_title = ctk.CTkLabel(self, text="Atenea Convert PNG ↔ WEBP",
                                        font=("Segoe UI", 21, "bold"), text_color="#2196F3")
        self.label_title.pack(pady=20)

        # --- INPUT FOLDER ---
        self.label_in = ctk.CTkLabel(self, text="📂 Input folder:", font=("Segoe UI", 14))
        self.label_in.pack()
        self.entry_in = ctk.CTkEntry(self, width=400)
        self.entry_in.insert(0, "original")
        self.entry_in.pack(pady=5)
        self.btn_in = ctk.CTkButton(self, text="Select folder", command=self.select_in)
        self.btn_in.pack(pady=5)

        # --- OUTPUT FOLDER ---
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
        self.formato = ctk.CTkOptionMenu(self, values=["PNG → WEBP", "WEBP → PNG"])
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

    def select_in(self):
        folder = filedialog.askdirectory()
        if folder:
            self.entry_in.delete(0, tk.END)
            self.entry_in.insert(0, folder)

    def select_out(self):
        folder = filedialog.askdirectory()
        if folder:
            self.entry_out.delete(0, tk.END)
            self.entry_out.insert(0, folder)

    def convert(self):
        carpeta_entrada = self.entry_in.get().strip()
        carpeta_salida = self.entry_out.get().strip()
        modo = self.formato.get()

        if not carpeta_entrada or not carpeta_salida:
            messagebox.showerror("Error", "Debe seleccionar ambas carpetas.")
            return

        try:
            convertir_png_webp(carpeta_entrada, carpeta_salida, modo)
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
