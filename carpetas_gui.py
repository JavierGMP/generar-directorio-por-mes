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

raw_image = "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MDI0LTA4LTEzVDE3OjE1OjQ5KzAwOjAwIfsvRQAAACV0RVh0ZGF0ZTptb2RpZnkAMjAyNC0wOC0xM1QxNzoxNTo0OSswMDowMFCml/kAAAAodEVYdGRhdGU6dGltZXN0YW1wADIwMjQtMDgtMTNUMTc6MTU6NDkrMDA6MDAHs7YmAAAARnRFWHRzb2Z0d2FyZQBJbWFnZU1hZ2ljayA2LjcuNy0wIDIwMTItMDUtMzAgUTE2IGh0dHA6Ly93d3cuaW1hZ2VtYWdpY2sub3JnwI8OHAAAABh0RVh0VGh1bWI6OkRvY3VtZW50OjpQYWdlcwAxp/+7LwAAABh0RVh0VGh1bWI6OkltYWdlOjpoZWlnaHQAMjU2pp5HyQAAABd0RVh0VGh1bWI6OkltYWdlOjpXaWR0aAAyNTZ6MhREAAAAGXRFWHRUaHVtYjo6TWltZXR5cGUAaW1hZ2UvcG5nP7JWTgAAABd0RVh0VGh1bWI6Ok1UaW1lADEzNTMxNzcxNDMpnOdQAAAAD3RFWHRUaHVtYjo6U2l6ZQAwQkKUoj7sAAAAXHRFWHRUaHVtYjo6VVJJAGZpbGU6Ly8vdXNyYmFja3VwL3Vzci9sb2NhbC93d3cveml6YXphL2FwcC9kYXRhL2ljb25zZXQvNTcyNjE0L1BORy8yNTYvNTcyNjIzLnBuZ49Don0AAAAASUVORK5CYII="




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
