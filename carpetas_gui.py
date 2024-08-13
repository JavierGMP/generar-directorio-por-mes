#Author: Javier García-Merás Palacios
#version : 0.1
#Description: Aplicación para el borrado masivo de carpetas vacias y creacion de carpetas de meses o dias


from tkinter import Image, Listbox, filedialog, font, messagebox, ttk, StringVar, TOP
import os
from functools import partial
from base64 import b64decode
import tempfile
import time
import datetime as dt

from PIL import Image, ImageTk
import tkinter as tk

raw_image = "iVBORw0KGgoAAAANSUhEUgAAAHwAAAAuCAMAAADdho1wAAAAV1BMVEVHcEz/OgD/OgD/OgD/OgD/OgD/OgD/OgD/OgD/OgD/OgD/OgD/OgD/OgD/OgD/OgD/OgD/OgD/OgD/OgD/OgD/OgD/OgD/OgD/OgD/OgD/OgD/OgD/OgD/maxbAAAAHHRSTlMAOZ4DJi3nBvftGwy7zNVo3RNcRk20w4eoe5JvWvIB4QAAA/5JREFUWMPNWNuypCoMbS94Q1QUUdT//85x79Y2IRG7ps6pmlQ/AWZ1FrmR1+tfk0RqrWX+H2nL5dfKdNQuo1VK2TF2pkqunUpckiJleQq2JNa2vrXVsRuqB5OjSZXbJUU3959Phq78SNbDr/rs2rEV0lYAZU08yHvsKIbIhzTuUJfHYFUBM9IGIPQhbUVtbvjXEwP9I6OkINt0GQj/VHwq1y7jdBVxyppteeitWM8jPSCxjM5VA1abU7UYb7RtzUCxTXd3ev5cFCL+5KNSDOlRs91K2RPs7O5sJ25ut32vTQzpUbdt36Pfnz4xKPHdL8VRSUlPmy0oJWK+stsz6YT4ZU8CcqSky3F7kAZ4XbL45pZZVhDSf06mgKLCvF4rQ7rzte3iLcVXxA0oxgrlBpGKqI87GLaHtECP1aKj5ogMh7YzUWRcjfB//vfB5YwcrNVvI/fbcBNJSRIedjHj6YhGaw4N0lgudyCf2SziOaExCY2FdJ5MIsNjkAgr+LeLgfmrSjyWnrYI+hC88VmjFArR42OtuQsCXhDxhHRpeaf2Q7B5czJA7pIvqr1gksLHfQW4w9X/dCW8r1zCDsoaCNweuC4p4BUw3f2uAI+10LmHtb1kNYATkkVARE7kWqEs3m5ec3VyjwGc7ev8fg/mDGBKyzirp1Aq9rhvHQJ/rcVNtsxHGk3wX1/fKek5O8hnfo7E4FrBvQUk/4vHgnEg4I6N9sDNLbEeuEEJuRFfgic+OEu7rrcQeKW80pdztJtn2lmHc1sInFbB677mQJijQHwrBP455lyZI+CGJNguZUJtTh5DDVqZvS8vd/X4lowD90lHwQZsy9JQklmJHe64uVNiBpyQjoiH6XUKhPkRiFXHd4v4Si5wUwaqWgILSxYFCoumTf+on8BRq/zQRNnqthwunP/E+gEckF442rPDUN6/AtdeQSM/JUyiBqeOLicF4X6CQ9LnvKevFUTk1hxNmd9GXZmhR6FTxqaS+f6qFqsioQZJ36+UtNIkORZq6gfSQILanXu9SdHZcaybksZ5At8nzu/oDH3DnL2ztwLjQDRPbf4BDkm32m8sjtaI5mZfsCOa8itwSPrR7iGkg3jRhXV1OAST/gn9p7tDpB9AKBWfxA9ZSFVGCn0fPF/8NuBDyTUQEzOwGAK2d0yTMajA+T73npNXHUtQqj/5uB017KHM9aTVckN9tqTE0+HjFQ0sziJe8UOWctJ3s6iZ+aBbBL3cDNYAFKmfSRGnrZwDvXkeTdYbhbXp8WLT4/5uPgX3CaIBWw5qQ6MwNUUPs0Ap+mmurVJ2XtYBDAFlCsR7vFZgC84NPyNFOy5tpL94De2/XO6SvP5CEm6Y+rfK/lf5A5RpN2/mmB9oAAAAAElFTkSuQmCC"




def borrado_carpetas(ruta):
    dir_path = ruta.get()
    
    if not os.path.exists(dir_path):
        messagebox.showerror("Sistema", f"El directorio no existe: {dir_path}")
    else:
        for root, dirs, files in os.walk(dir_path, topdown=False):
            for dir_name in dirs:
                carpeta = os.path.join(root, dir_name)
                if len(os.listdir(carpeta)) == 0:
                    try:
                        os.rmdir(carpeta)
                    except OSError as e:
                        messagebox.showerror("Sistema", f"Error al eliminar la carpeta: {e}")
        messagebox.showinfo("Sistema", f"Carpetas eliminadas en: {dir_path}")

def crear_carpetas_mes(ruta):
    
    dir_path=ruta.get()
    
    meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]

    try: 
        num = 1
        os.makedirs(dir_path, exist_ok=True)
        for mes in meses:
            path_full = os.path.join(dir_path, f"{str(num).zfill(2)}. {mes}")
            num = num + 1
            os.makedirs(path_full, exist_ok=True)
        messagebox.showinfo("Sistema", f"Carpetas creadas en: {dir_path}")    
    except KeyboardInterrupt:
        messagebox.showerror("Sistema", "Saliendo del programa...")

def crear_carpetas_dia(path, anno, mes):
    ruta = path.get()
    year = int(anno.get())
    month = int(mes.get())
    # Obtener el número de días en el mes y año dados
    num_dias = obtener_dias_en_mes(year, month)
    
    # Crear las carpetas
    for dia in range(1, num_dias + 1):
        fecha = dt.datetime(year, month, dia)
        formato_fecha = fecha.strftime("%Y-%m-%d")
        nueva_ruta = os.path.join(ruta, formato_fecha)
        
        # Crear la carpeta si no existe
        if not os.path.exists(nueva_ruta):
            os.makedirs(nueva_ruta)
        else:
            messagebox.showerror("Sistema", f"Carpeta ya existe: {nueva_ruta}")
    messagebox.showinfo("Sistema", f"Carpetas creadas en: {ruta}")         

def obtener_dias_en_mes(year, month):
    # Calcula el número de días en el mes y año dados
    if month == 12:
        next_month = 1
        next_year = year + 1
    else:
        next_month = month + 1
        next_year = year
    
    # Primer día del próximo mes
    primer_dia_siguiente_mes = dt.datetime(next_year, next_month, 1)
    
    # Último día del mes actual
    ultimo_dia_mes_actual = primer_dia_siguiente_mes - dt.timedelta(days=1)
    
    return ultimo_dia_mes_actual.day

def borrado_masivo():
    app2 =tk.Toplevel(app)
    app2.title("Borrado de Carpetas")
    app2.geometry("400x270")
    app2.resizable(width=False, height=False)
    
    icon_borrado = "AAABAAEAEBAAAAEAIABoBAAAFgAAACgAAAAQAAAAIAAAAAEAIAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAWAAAAFgAAABYAAAAWAAAAFgAAABYAAAAWAAAAFgAAABYAAAAWAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACbAAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAJIAAAAAAAAAAAAAAAAAAAAAAAAAtwAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAACuAAAAAAAAAAAAAAAAAAAAAAAAANMAAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAAygAAAAAAAAAAAAAAAAAAAAAAAADvAAAA/wAAAP8AAAD/AAAA+gAAAP8AAAD/AAAA+wAAAP8AAAD/AAAA/wAAAOYAAAAAAAAAAAAAAAAAAAAAAAAA/wAAAP8AAAD/AAAA/wAAAHgAAABUAAAATQAAAH8AAAD/AAAA/wAAAP8AAAD+AAAAAAAAAAAAAAAAAAAAAAAAAP8AAAD/AAAA/wAAAP8AAAD/AAAAFwAAABsAAAD/AAAA/wAAAP8AAAD/AAAA/wAAAAAAAAAAAAAAAAAAAAAAAAD/AAAA/wAAAP8AAAD/AAAA+wAAAAAAAAAAAAAA/QAAAP8AAAD/AAAA/wAAAP8AAAAAAAAAAAAAAAAAAAAAAAAA/wAAAP8AAAD/AAAA/wAAAEEAAADxAAAA7QAAAEoAAAD/AAAA/wAAAP8AAAD/AAAAAAAAAAAAAAAAAAAAAAAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAAAAAAAAAAAAAAAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAAAAAAABUAAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAA0AAABXAAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAABPAAAAOQAAAJUAAACVAAAAlQAAAMsAAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAACVAAAAlQAAAJUAAACVAAAAMwAAAAAAAAAAAAAAAAAAAAAAAACAAAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACcAAAAnAAAAJwAAACcAAAAnAAAAEwAAAAAAAAAAAAAAAAAAAAAAAAAA4AcAAMADAADAAwAAwAMAAMADAADAAwAAwAMAAMGDAADAAwAAwAMAAIABAAAAAAAAAAAAAAAAAADwHwAA+B8AAA=="

    icon_path2 = os.path.join(tempfile.gettempdir(), "app2_icon.ico")
    with open(icon_path2, "wb") as icon2_file:
        icon2_file.write(b64decode(icon_borrado))
        
    app2.iconbitmap(icon_path2)
    
    label2 = ttk.Label(
        app2,
        text="Ingrese ruta:",
        foreground="black",
        font=("Helvetica", 20, "bold"),
    )
    label2.place(x=105, y=37)
    
    ruta = tk.Entry(
        app2,
        width=40, 
        font=font.Font(family="Times", size=12),
        justify=tk.CENTER,
        )
    ruta.place(x=20, y=80)
    
    button_borrado = tk.Button(
        app2,
        text = "Borrado",
        command=partial(borrado_carpetas, ruta),
        width=18
    )
    button_borrado.place(x=25, y=135)
    
    button_salir = tk.Button(
        app2,
        text= "Salir",
        fg="red",
        command=app2.destroy,
        width=18
    )
    button_salir.place(x=230, y=135)
    
    button_borrar = tk.Button(
        app2,
        text="Limpiar Texto",
        
        width=18
    )
    button_borrar.place(x=25, y=180)
    button_borrar.config(command=lambda: ruta.delete(0, tk.END))
    
    app2.mainloop()
    
    
def crear_carpetas_por_mes():
    app3 = tk.Toplevel(app)
    app3.title("Crear carpetas por mes")
    app3.geometry("400x270")
    app3.resizable(height=False, width=False)
    
    icon_crear_carpeta = "AAABAAEAEBAAAAEAIABoBAAAFgAAACgAAAAQAAAAIAAAAAEAIAAAAAAAAAQAANcNAADXDQAAAAAAAAAAAAAAAACAAAAA5gAAAPIAAADxAAAA8QAAAPEAAADxAAAA8QAAAPEAAADxAAAA8QAAAPEAAADxAAAA8gAAAOYAAACAAAAA5gAAAJIAAABNAAAATgAAAE4AAABOAAAATAAAAEwAAABOAAAATgAAAE4AAABOAAAATgAAAE0AAACSAAAA5gAAAPEAAABOAAAAAAAAAAAAAAAAAAAAAAAAACMAAAAzAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAATgAAAPEAAADxAAAATgAAAAAAAAAAAAAAAAAAAC0AAAC6AAAA0QAAAD8AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAE4AAADxAAAA8QAAAE4AAAAAAAAAAAAAADQAAAC9AAAAuAAAALAAAADDAAAAMQAAAAAAAAAAAAAAAAAAAAAAAABOAAAA8QAAAPEAAABOAAAAAAAAAAsAAACaAAAArgAAACMAAAAeAAAAsAAAALgAAAAlAAAAAAAAAAAAAAAAAAAATgAAAPEAAADxAAAATgAAAAAAAAACAAAALwAAAB4AAAAAAAAAAAAAACoAAAC+AAAAqQAAABsAAAAAAAAAAAAAAE4AAADxAAAA8QAAAE4AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAANwAAAMkAAACQAAAACgAAAAAAAABOAAAA8QAAAPEAAABNAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABBAAAAYgAAAAcAAAAAAAAATQAAAPEAAADyAAAAXQAAABMAAAAWAAAAFgAAABYAAAAWAAAAFgAAABYAAAAWAAAAFgAAABcAAAAWAAAAEwAAAF0AAADyAAAA+wAAANMAAAC/AAAAvwAAAMAAAADAAAAAwAAAAMAAAADAAAAAwAAAAMAAAADAAAAAvwAAAL8AAADTAAAA+wAAAPYAAACVAAAAagAAAHAAAABoAAAAZwAAAGcAAABnAAAAZwAAAGcAAABnAAAAaAAAAHAAAABqAAAAlQAAAPYAAADyAAAATgAAAEIAAACDAAAADgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA4AAACDAAAAQgAAAE4AAADyAAAA1wAAALQAAAC0AAAA4QAAAI0AAACBAAAAggAAAIIAAACCAAAAggAAAIEAAACNAAAA4QAAALQAAAC0AAAA1wAAAEgAAACcAAAA0AAAAOsAAAC2AAAArgAAAK8AAACvAAAArwAAAK8AAACuAAAAtgAAAOsAAADQAAAAnAAAAEgAAAAAAAAABgAAAG8AAADDAAAAIgAAAAsAAAAMAAAADAAAAAwAAAAMAAAACwAAACIAAADDAAAAbwAAAAYAAAAAAAAAAAAAAAA8fAAAOHwAADA8AAAgHAAAIwwAAD+EAAA/xAAAAAAAAAAAAAAAAAAAB+AAAAAAAAAAAAAAgAEAAA=="

    icon_path2 = os.path.join(tempfile.gettempdir(), "app3_icon.ico")
    with open(icon_path2, "wb") as icon2_file:
        icon2_file.write(b64decode(icon_crear_carpeta))
        
    app3.iconbitmap(icon_path2)
    
    label2 = ttk.Label(
        app3,
        text="Ingrese ruta:",
        foreground="black",
        font=("Helvetica", 20, "bold"),
    )
    label2.place(x=105, y=37)
    
    ruta = tk.Entry(
        app3,
        width=40, 
        font=font.Font(family="Times", size=12),
        justify=tk.CENTER,
        )
    ruta.place(x=20, y=80)
    
    button_crear_carpeta = tk.Button(
        app3,
        text = "Crear",
        command=partial(crear_carpetas_mes, ruta),
        width=18
    )
    button_crear_carpeta.place(x=25, y=135)
    
    button_salir = tk.Button(
        app3,
        text= "Salir",
        fg="red",
        command=app3.destroy,
        width=18
    )
    button_salir.place(x=230, y=135)
    
    button_borrar = tk.Button(
        app3,
        text="Limpiar Texto",
        
        width=18
    )
    button_borrar.place(x=25, y=180)
    button_borrar.config(command=lambda: ruta.delete(0, tk.END))
    
    app3.mainloop()


def crear_carpetas_por_dia():
    def limpiar_texto():
        ruta.delete(0, tk.END)
        mes.delete(0, tk.END)
        anno.delete(0, tk.END)
    
    app4 = tk.Toplevel(app)
    app4.title("Crear carpetas por mes")
    app4.geometry("400x400")
    app4.resizable(height=False, width=False)
    
    icon_crear_carpeta_dia = "AAABAAEAEBAAAAEACABoBQAAFgAAACgAAAAQAAAAIAAAAAEACAAAAAAAAAEAANcNAADXDQAAAAEAAAABAAD5pgAA8pQAAPmmAAD4pgAA/6MAAG+0jAAEu/kAFbHoAP+fAADqqBEACLz0AAi19QDjmhYA+p4AAPObAADzmgAA+aYAAPmmAAD4pgAA+6UAANynHQAvs80AfZ56AP2hAAD0pAQATbKtAEukrgDvlwUA85oAAPKYAADxlgAA8JQAAPmlAAD5pgAA75IAAO+RAAD5pgAA+aUAAO2MAADsiwAA+KUAAPikAADqhwAA6oYAAPaiAAD2oQAA6IIAAOeAAADznAAA85sAAOZ8AADlewAA8pcAAPGTAADkeAAA5HgAAPeiAADzkwAA534AAOd9AAD4pgAA96MAAOd+AADmfQAA+KUAAPejAADmfQAA5nsAAPekAAD2ogAA5XsAAOV6AAD3owAA5HgAAPOaAQDnlAoA23cKAON2AQDZjyoArJVuALCffgCvnn0ArJp5AKqZeACpmHcAqJd2AKiWdgCnlXUAppR0AKaTcwCoj2oAz3smALm8swC3uKwAtLWoALe4qgC2t6kAtLanALK0pQCxsqMAsLGiAK6voACsrp4Aq6ydAKqrmwCoqZkAp6mYAKWpmgD5pgAA+aUAAPCmCACZpl8AxpkuAPigAAD1oQAAraNJAKmWSgDxlQAA8ZcAAPCUAAD4pQAA96QAAPWfAAD0nAAA85oAAPKXAADwkwAA75EAAO2PAAD2ogAA9qwmAPe+WQD1tkoA8ZsQAPCUAwDyqDQA75kZAOyLAADriQAA85wAAPSnIgD53KkA99CRAPnZqQD1xHgA8q5JAPrmxwDwqkoA6oQAAOmEAADymQAA9LNKAPjYpwDulQ8A8axGAPfYqwDwqEYA+Ny2AO+oTgDnfwAA5n4AAPCRAADujgAA8rFPAPbRnQDsjQcA76I5APbVqADrkR4A9M2bAO2mTwDlewAA5XoAAO+FAADugwAA8apNAPTOmgDujAcA8KI4APTTpQDulR4A882ZAO6pTQDogQAA54AAAPOUAADvhgAA86pKAPjWpwDwkQ8A8qpGAPjXqgDvlxwA8KxPAOmCAADylAAA8psiAPnYqgD3zJAA+NeoAPXCeQDtkQ4A9s6WAO+pSwD0mwAA8ZQAAPKgKAD0tlsA869MAO6TEADsiwIA7p0vAOuPFwDnfgAA9qEAAPWeAADxkgAA8I4AAO+MAADtiwAA7IkAAOuFAADogAAA530AAOOSDwDkkhAA448QAOGMDgDfiQ4A3ocOAN6FDgDdgw4A3IAOANp+DgDafA4A2HoOAKiYdwClknMA////AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAXF1eX2BhYmNkZWZnaGlqa05P7FBRUlNUVVZXWFntWltKS+Dh4uPk5ebn6Onq60xNSNbXzH3Y2drb3N3C3t+sSURFeszNzs/Q0dLT1LfVRkdAQXrDxMXGx8jJysu3uEJDPD25uru8vb6/wKTBwrc+Pzg5ra6vsLGys7S1tre4Ojs0NaGio6SlpqeoqaqrrDY3MDGWdZeYmZqbnJ2en6AyMywteouMjY6PkJGSk5SVLi8oKXmBeoKDhIWGh4iJiiorJCV4eHl6e3t8fX5+f4AmJyAhbG1ub3BxcnN0dXZ3IiMQERITFBUWFxgZGhscHR4fAAIDBAUGBwgJCgsMDQ4PAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIABAAA="

    icon_path2 = os.path.join(tempfile.gettempdir(), "app4_icon.ico")
    with open(icon_path2, "wb") as icon2_file:
        icon2_file.write(b64decode(icon_crear_carpeta_dia))
        
    app4.iconbitmap(icon_path2)
    
    label2 = ttk.Label(
        app4,
        text="Ingrese ruta:",
        foreground="black",
        font=("Helvetica", 20, "bold"),
    )
    label2.place(x=105, y=30)
    
    ruta = tk.Entry(
        app4,
        width=40, 
        font=font.Font(family="Times", size=12),
        justify=tk.CENTER,
        )
    ruta.place(x=20, y=67)
    
    label3 = ttk.Label(
        app4,
        text="Ingrese año (Ej: 2024):",
        foreground="black",
        font=("Helvetica", 20, "bold"),
    )
    label3.place(x=55, y=120)
    
    anno = tk.Entry(
        app4,
        width=40, 
        font=font.Font(family="Times", size=12),
        justify=tk.CENTER,
        )
    anno.place(x=20, y=157)
    
    label4 = ttk.Label(
        app4,
        text="Ingrese mes en numero (Ej: 7 para julio):",
        foreground="black",
        font=("Helvetica", 14, "bold"),
    )
    label4.place(x=15, y=200)
    
    mes = tk.Entry(
        app4,
        width=40, 
        font=font.Font(family="Times", size=12),
        justify=tk.CENTER,
        )
    mes.place(x=20, y=237)
    
    button_crear_carpeta = tk.Button(
        app4,
        text = "Crear",
        command=partial(crear_carpetas_dia, ruta, anno, mes),
        width=18
    )
    button_crear_carpeta.place(x=25, y=305)
    
    button_salir = tk.Button(
        app4,
        text= "Salir",
        fg="red",
        command=app4.destroy,
        width=18
    )
    button_salir.place(x=230, y=305)
    
    button_borrar = tk.Button(
        app4,
        text="Limpiar Texto",
        width=18,
        command=limpiar_texto,
    )
    button_borrar.place(x=25, y=345)
 
    
    app4.mainloop()




app = tk.Tk()

icon_main ="AAABAAEAEBAAAAEACABoBQAAFgAAACgAAAAQAAAAIAAAAAEACAAAAAAAAAEAAMMOAADDDgAAAAEAAAABAAAAAAAAL9u6ABGwWAD44HQA+d+HANyoTQDZp0YAALD8ACrbuwA027kADrNdABKvVgD/4GgArt6NAGvcpQBCoUYASKJIAE/WowBPyo4AUcmLAE3JkQD74W8A9+BzAO3fdQBbsWwAQ8GWAD3GpQBAxaEAQ8OdAE3CkAAm2P8Ag9zCAKrdpwBOvYwAK9j+AC3Y/AAt1/sAVbl/ACvY/wBerWoAKdf/AGihVwAm1f8Aa6FWACPT/gBuoVQAINL9AHCgUQAe0PwAdZpHABvP/ACqmj4AeokyABjN/AC7tXEAx6FDAHJ1HwAWy/wAGbzoALCydQDoslEAEcT8AAe49QBesaoA/50AAAq0/AAIsf0AAKv8AACs/AAAsv0ANdy5ADXbuAA02rUAH8+aABDCfABm3KYAZ9qjAGbUnQBkzZQAVMB0ADm1XwDr3HQA6tpxAOfQZgDes0QA354eALWZIQCp26UAp9ikAJ7RogCYxJsAnaJ2AMWVMAC/lB8AdLBpAES6rwA7uL0ANLe/AC63ugAr1vsAKNT6ABjG+QAHrvgAEofyAHKLiwDatUwA3chxANPHfQDPxYAAur95AGy2fgAp1/8AJtb/ACPT/gAh0v4AFsX9AAiq/AAdg/YAUoaqAJuxeAC72MAAwNnBANzWqgDsx3UAmq5YACfW/wAk0/4AIdL9AB7Q/QAbzv0AF8n9ABjE/AApsvQANaftADer9QA1q/YAVrrHAM62WwCfqlEAJNT+ABzP/QAZzf4AFsz+ABPL/gAnrPwANJP5ADKS+AAukvoAJLHiAKqoXQCcpk0AE8r+ABHI/QAPxf0ADMP8AArB+wAFwP0AG7zlAKinYQCZokwAEcj+AA7H/QALxf0ACcT8AAbC/AABwP4AGrznAK+saACdpE0ADMX9AAbB/AADwP0AAL/+ABu85wC0sG0Ao6NKABnN/QABvvwAAL7+ABu86AC4s28AFsz9AAG+/QAAvvwAHL3oABPK/QABv/0AAL79AA/D/QAMwf0ACr/9AAi+/AAFvfwAA7v8AAG6/AAAufwABrD9AASu/QADrv0AAa39AACs/QAAq/0A////AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQULExcbHyMnJyclDREUHAD28vb6/wMHCw8PDwz4/QAY5uaChqaOkq7q7u7I6OzwFNbWXoKGpo6qrtreyuDY3ODKwjpegoamjqquxsrO0MzQwjI2Ol6ChqaOqq6ytrq8xLoCMjY6XoKGio6SlpqeoLyxygIyNjpeYmZqbnJ2eny0qi3+AjI2Oj5CRkpOUlZYrKH1+f4CBgoOEhYaHiImKKSZvcHFyc3R1dnd4eXp7fCciIyRjZGVmZ2hpamtsbW4lHh8gV1hZWltcXV5fYGFiIQQVFhdRUlNUVVYYGRobHB0DDA0OS0xNTk9QDxAREhMUAAEICUZGR0hJSgoLAgAAAAADAAAAAQAAAAEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACAAAAAgAAAAMAPAAA="

icon_path = os.path.join(tempfile.gettempdir(), "app_icon.ico")
with open(icon_path, "wb") as icon_file:
    icon_file.write(b64decode(icon_main))

app.geometry("450x300")
app.title("Gestión de Carpetas")
app.resizable(width=False, height=False)

app.iconbitmap(icon_path)

label = ttk.Label(
    app,
    text="Gestión de Carpetas",
    foreground="black",
    font=("Helvetica", 20, "bold"),
)
label.place(x=60, y=40)

button_zooplus = tk.Button(
    app,
    text="Borrado Masivo",
    command=borrado_masivo,
    width=16
   
)
button_zooplus.place(x=50, y=100)

button_nike = tk.Button(
    app,
    text="Creación por mes",
    command=crear_carpetas_por_mes,
    width=16
   
)
button_nike.place(x=50, y=140)

button_electrolux = tk.Button(
    app,
    text="Creación por día",
    command=crear_carpetas_por_dia,
    width=16
    
)
button_electrolux.place(x=250, y=100)

raw_image_data = b64decode(raw_image)
with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp_image_file:
    temp_image_file.write(raw_image_data)
    temp_image_path = temp_image_file.name

image = Image.open(temp_image_path)
photo = ImageTk.PhotoImage(image)

label2 = tk.Label(app, image=photo, text="")#type: ignore
label2.place(x=275, y=185)

button_salir = tk.Button(
    app,
    text="Salir",
    command=app.destroy,
    width=12,
    foreground="red"
    
)
button_salir.place(x=270, y=250)

app.mainloop()
