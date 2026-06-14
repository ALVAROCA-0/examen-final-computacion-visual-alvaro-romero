import tkinter as tk
from tkinter import font as tkf
import customtkinter as ctk
from tkinterdnd2 import TkinterDnD, DND_ALL
from collections.abc import Iterable
from pathlib import Path
from collections.abc import Callable
import cv2
import numpy as np
from PIL import Image as P_Im

def hex2rgb(h: str) -> list[int, int, int]:
    h = h.removeprefix("#")
    return list(map(lambda x: int(x,16), (h[i:i+2] for i in range(0,6,2))))

def rgb2hex(rgb: list[int, int, int]) -> str:
    return "#{:02x}{:02x}{:02x}".format(*map(lambda x: max(min(int(x), 255), 0),rgb))

def rgb16_2rgb(rgb: int):
    return [(rgb//65536) % 256, (rgb//256) % 256, rgb % 256]

def trunk_path(path: Path, max_size: int, get_size: Callable[[str], int] = len) -> str:
    parts = reversed(path.parts)
    ret = next(parts)
    for part in parts:
        updt = part + "\\" + ret
        if get_size("...\\" + updt) > max_size:
            ret = "...\\" + ret
            break
        else:
            ret = updt
    return ret

class Image(ctk.CTkLabel):
    def __init__(self, master=None, image=None, **kwargs):
        kwargs["text"] = ""
        width = kwargs["width"] if "width" in kwargs else self.cget("width")
        height = kwargs["height"] if "height" in kwargs else self.cget("height")
        
        self.image = np.zeros((height, width, 3), dtype=np.uint8)
        self.ctk_im = ctk.CTkImage(P_Im.fromarray(self.image), size=(width, height))
        self.set_image(image)
        super().__init__(master=master, image=self.ctk_im, **kwargs)
        
    def set_image(self, image):
        if image is None:
            return

        if isinstance(image, str):
            image = cv2.imread(image)

            if image is None:
                return

            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        self.image = image

        self.ctk_im.configure(
            light_image=P_Im.fromarray(image),
            size=(self.cget("width"), self.cget("height"))
        )
            

class FileDrop(ctk.CTkFrame):
    def __init__(self, master = None, *, ends_with: Iterable[str]|str|None = None, load:Callable[[str]]|None= None, width=None, **kwargs):
        self.path: Path | None = None
        self.lbl_font = tkf.Font(family="Arial", size=10, weight="normal")
        self.load = load
        
        if width is not None and width < 80: width = 80
        super().__init__(master, width=(width-40 if width is not None else 200), **kwargs)
        self.ends_with = ends_with
        
        self.upper = ctk.CTkFrame(self, bg_color="transparent", fg_color="transparent")
        self.upper.pack(fill="x", anchor="n", padx=20, pady=(10,0))
        
        #entry for drag and drop
        self.entry = ctk.CTkEntry(self.upper, placeholder_text="Drop a file here", width=(width-40 if width is not None else 140), border_width=0, placeholder_text_color="lightgray")
        self.entry.configure(justify="center")
        self.entry.pack(side="left", fill="x", anchor="w", padx=(0, 5))
        
        if load is not None:
            self.button = ctk.CTkButton(self.upper, 28, text="↑", command=lambda: (load(self.path.absolute()), self.label.configure(text_color="SpringGreen")))
            self.button.pack(side="right", anchor="e", padx=(5, 0))
            
        #Label to display actions taken 
        self.label = ctk.CTkLabel(self, text="", font=("Arial", 10), width=(width-40 if width is not None else 140), height=10)
        self.label.pack(side="bottom", fill="x", anchor="n", padx=20, pady=(0,10))
        
        #bindings
        self.entry.drop_target_register(DND_ALL)
        self.entry.dnd_bind("<<Drop>>", self.handle_drop)
        self.entry.bind("<Enter>", self.handle_enter)
        self.entry.bind("<Leave>", self.handle_leave)
        self.entry.bind("<Button-1>", lambda x: "break")
        self.entry.bind("<Button-2>", lambda x: "break")
        self.entry.bind("<ButtonRelease-1>", self.call_file_dialog)
        self.entry.bind("<ButtonRelease-2>", self.call_file_dialog)
    
    def handle_enter(self, event: tk.Event):
        light, dark = (list(x//256 for x in self.winfo_rgb(col)) for col in self.entry.cget("fg_color"))
        
        light = rgb2hex(map(lambda x: x - 5, light))
        dark = rgb2hex(map(lambda x: x - 5, dark))
            
        # print(color)
        self.entry.configure(fg_color=(light, dark))
    
    def handle_leave(self, event: tk.Event):
        light, dark = (list(x//256 for x in self.winfo_rgb(col)) for col in self.entry.cget("fg_color"))
        
        light = rgb2hex(map(lambda x: x + 5, light))
        dark = rgb2hex(map(lambda x: x + 5, dark))
            
        # print(color)
        self.entry.configure(fg_color=(light, dark))
    
    def call_file_dialog(self, event: tk.Event):
        file_path = ctk.filedialog.askopenfilename(filetypes=list(("Image file", ext)for ext in self.ends_with))
        if file_path != "":
            self.path = Path(file_path)
            self.label.configure(text=trunk_path(self.path, self.label.cget("width"), self.lbl_font.measure), text_color="white")
        return "break"
    
    def handle_drop(self, event: tk.Event):
        # Clean bracket wrap artifact injected by Tcl for files containing spaces
        file_path: str = event.data.strip("{}") 
        
        if self.ends_with is not None and not file_path.endswith(self.ends_with if isinstance(self.ends_with, str) else tuple(self.ends_with)):
            self.label.configure(text=f"Error: El archivo no es del tipo esperado", text_color="red")
            return
        
        self.path = Path(file_path)
        
        # Update text label
        self.label.configure(text=file_path, text_color="white")

class App(ctk.CTk, TkinterDnD.DnDWrapper):
    def __init__(self):
        super().__init__()
        self.TkdndVersion = TkinterDnD._require(self)
        self.palette = {
            # Base color palette (custom theme)
            "color01": "#1C2736",
            "color02": "#252F3D",
            "color03": "#2F3744",
            "color04": "#39404B",
            "color05": "#424852",
            "color06": "#4C515A",
            "color07": "#565A61",
            "color08": "#616469",
            "color09": "#6B6D70",
            "color10": "#757678",
            "color11": "#808080",
        }
        
        self.title("Punto 1 examen final")
        self.geometry("500x450")
        
        #accesso a imagenes
        self.original = None
        self.gray = None
        self.hsv = None
        self.blur = None
        self.edges = None
        self.segmented = None
        
        #manejo de tabs
        self.tabs = ctk.CTkTabview(self)
        self.tabs.pack(fill="both", expand=True)
        #acceso para cada tab
        self.load = self.tabs.add("Cargar Imagen")
        self.pre = self.tabs.add("Pre-Procesado")
        self.border = self.tabs.add("Detección bordes")
        self.seg = self.tabs.add("Segmentación")
        self.res = self.tabs.add("Resultados")
        #tab por default
        self.tabs.set("Cargar Imagen")
        
        #tab de carga
        self.loaded = Image(self.load, width=300, height=300)
        self.file = FileDrop(
            self.load,
            ends_with=[".png", ".jpg", ".jpeg"],
            fg_color=None,
            width=300,
            load=self.process_image
        )
        
        self.file.pack(anchor="n", pady=(20, 0), padx=20) 
        self.loaded.pack(anchor="s", fill="both", pady=20, padx=20)
        
        #tab de pre procesamiento
        self.color_mode = ctk.StringVar(value="HSV")

        ctk.CTkLabel(self.pre, text="Espacio de color:").pack(pady=(10,0))

        self.color_dropdown = ctk.CTkOptionMenu(
            self.pre,
            variable=self.color_mode,
            values=["HSV", "LAB"],
            command=self.on_parameter_change
        )
        self.color_dropdown.pack()
        
        gray_frame = ctk.CTkFrame(self.pre)
        gray_frame.pack(side="left", padx=10, pady=20)

        self.gray_view = Image(gray_frame, width=220, height=220)
        self.gray_view.pack()

        ctk.CTkLabel(gray_frame, text="Escala de Grises").pack(pady=(5,0))
        
        hsv_frame = ctk.CTkFrame(self.pre)
        hsv_frame.pack(side="right", padx=10, pady=20)

        self.hsv_view = Image(hsv_frame, width=220, height=220)
        self.hsv_view.pack()

        self.hsv_label = ctk.CTkLabel(hsv_frame, text="Representacion HSV")
        self.hsv_label.pack(pady=(5,0))
        
        #tab de calculo de bordes
        
        self.blur_method = ctk.StringVar(value="Gaussian")

        ctk.CTkLabel(self.border, text="Suavizado:").pack()

        self.blur_dropdown = ctk.CTkOptionMenu(
            self.border,
            variable=self.blur_method,
            values=["Gaussian", "Median"],
            command=self.on_parameter_change
        )

        self.blur_dropdown.pack()
        
        self.edge_method = ctk.StringVar(value="Canny")

        ctk.CTkLabel(self.border, text="Detector de bordes:").pack()

        self.edge_dropdown = ctk.CTkOptionMenu(
            self.border,
            variable=self.edge_method,
            values=["Canny", "Sobel"],
            command=self.on_parameter_change
        )

        self.edge_dropdown.pack()
        
        self.temp = ctk.CTkFrame(self.border, bg_color="transparent", fg_color="transparent")
        self.temp.pack(fill="x", expand=True)
        
        self.blur_label = ctk.CTkLabel(self.temp, text="Filtro Gaussiano")
        self.blur_label.pack(side="left", pady=(5,0), padx=(100,0))
        
        self.edge_label = ctk.CTkLabel(self.temp, text="Detector Canny")
        self.edge_label.pack(side="right", pady=(5,0), padx=(0,100))
        
        self.blur_view = Image(self.border, width=220, height=220)
        self.blur_view.pack(side="left", padx=10, pady=20)

        self.edge_view = Image(self.border, width=220, height=220)
        self.edge_view.pack(side="right", padx=10, pady=20)
        
        
        #tab de calculo de segmentacion
        self.seg_method = ctk.StringVar(value="Otsu")

        ctk.CTkLabel(self.seg, text="Método:").pack()

        self.seg_dropdown = ctk.CTkOptionMenu(
            self.seg,
            variable=self.seg_method,
            values=["Otsu", "Adaptive Threshold"],
            command=self.on_parameter_change
        )

        self.seg_dropdown.pack()
        
        self.seg_label = ctk.CTkLabel(self.seg, text="Umbralización Otsu")
        self.seg_label.pack(pady=(5,0))
        
        self.seg_view = Image(self.seg, width=300, height=300)
        self.seg_view.pack(pady=20)
        
        #tab de calculo de resultados
        self.result_label = ctk.CTkLabel(
            self.res,
            text="Resultados guardados en carpeta results"
        )

        self.result_label.pack(pady=20)
    
    def process_image(self, path):
        img = cv2.imread(path)
        if img is None: return

        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.original = img_rgb

        #Escala de grises
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        self.gray = gray

        #HSV
        if self.color_mode.get() == "HSV":
            color_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            color_vis = cv2.cvtColor(color_img, cv2.COLOR_HSV2RGB)
        else:
            color_img = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
            color_vis = cv2.cvtColor(color_img, cv2.COLOR_LAB2RGB)

        self.hsv = color_vis

        #Suavizado
        if self.blur_method.get() == "Gaussian":
            self.blur = cv2.GaussianBlur(gray, (5,5), 0)
        else:
            self.blur = cv2.medianBlur(gray, 5)

        #Bordes
        if self.edge_method.get() == "Canny":
            self.edges = cv2.Canny(self.blur, 100, 200)
        else:
            sobelx = cv2.Sobel(self.blur, cv2.CV_64F, 1, 0, ksize=3)

            sobely = cv2.Sobel(self.blur, cv2.CV_64F, 0, 1, ksize=3)

            self.edges = cv2.magnitude(sobelx, sobely)

            self.edges = cv2.convertScaleAbs(self.edges)

        #Segmentación (Otsu)
        if self.seg_method.get() == "Otsu":
            _, self.segmented = cv2.threshold(self.blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        else:
            self.segmented = cv2.adaptiveThreshold(self.blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

        self.show_results()
        self.save_results()
    
    def on_parameter_change(self, _):
        self.update_labels()

        if self.file.path:
            self.process_image(str(self.file.path))
    
    def update_labels(self):
        color_text = {"HSV": "Representación HSV", "LAB": "Representación CIELAB"}

        blur_text = {"Gaussian": "Filtro Gaussiano", "Median": "Filtro Mediana"}

        edge_text = {"Canny": "Detector Canny", "Sobel": "Detector Sobel"}

        seg_text = {"Otsu": "Umbralización Otsu", "Adaptive Threshold": "Umbralización Adaptativa"}

        self.hsv_label.configure(text=color_text[self.color_mode.get()])

        self.blur_label.configure(text=blur_text[self.blur_method.get()])

        self.edge_label.configure(text=edge_text[self.edge_method.get()])

        self.seg_label.configure(text=seg_text[self.seg_method.get()])
    
    def show_results(self):
        self.loaded.set_image(self.original)

        self.gray_view.set_image(
            cv2.cvtColor(self.gray, cv2.COLOR_GRAY2RGB)
        )

        self.hsv_view.set_image(self.hsv)

        self.blur_view.set_image(
            cv2.cvtColor(self.blur, cv2.COLOR_GRAY2RGB)
        )

        self.edge_view.set_image(
            cv2.cvtColor(self.edges, cv2.COLOR_GRAY2RGB)
        )

        self.seg_view.set_image(
            cv2.cvtColor(self.segmented, cv2.COLOR_GRAY2RGB)
        )
    def save_results(self):
        output = (Path(__file__).parent / ".." / "resultados").resolve()
        print(output)
        output.mkdir(exist_ok=True)

        cv2.imwrite(
            str(output/"gray.png"),
            self.gray
        )

        cv2.imwrite(
            str(output/"blur.png"),
            self.blur
        )

        cv2.imwrite(
            str(output/"edges.png"),
            self.edges
        )

        cv2.imwrite(
            str(output/"segmented.png"),
            self.segmented
        )

        hsv_bgr = cv2.cvtColor(
            self.hsv,
            cv2.COLOR_RGB2BGR
        )

        cv2.imwrite(
            str(output/"hsv.png"),
            hsv_bgr
        )

def main():
    app = App()
    app.mainloop()

if __name__ == "__main__":
    main()