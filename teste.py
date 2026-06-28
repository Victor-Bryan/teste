from tkinter import *
from tkinter import ttk

# Quando mouse é pressionado
def iniciar_figura_nova(event): 
    global figura_nova
    cor = cor_borda_var.get()
    cor_preench = cor_preench_var.get()
    if tipo_figura_var.get() == 'Linha':
        figura_nova = ("linha", (event.x, event.y, event.x, event.y), cor, cor_preench)
    elif tipo_figura_var.get() == 'Retangulos':
        figura_nova = ('Retangulos', (event.x, event.y, event.x, event.y), cor, cor_preench)
    elif tipo_figura_var.get() == 'Ovais':
        figura_nova = ('Ovais', (event.x, event.y, event.x, event.y), cor, cor_preench)
    elif tipo_figura_var.get() == 'Circulos':
        figura_nova = ('Circulos', (event.x, event.y, event.x, event.y), cor, cor_preench)
    else :
        figura_nova = ("rabisco", [(event.x, event.y)], cor, cor_preench)

# Quando mouse é movido com o botão pressionado
def atualizar_figura_nova(event):
    global figura_nova
    if figura_nova[0] == "rabisco":
        figura_nova[1].append((event.x, event.y))
        figura_nova = ('rabisco', figura_nova[1], figura_nova[2], figura_nova[3])
    elif figura_nova[0] == 'Retangulos':
        figura_nova = ('Retangulos', (figura_nova[1][0], figura_nova[1][1], event.x, event.y), figura_nova[2], figura_nova[3])
    elif figura_nova[0] == 'Ovais':
        figura_nova = ('Ovais',(figura_nova[1][0], figura_nova[1][1], event.x, event.y), figura_nova[2], figura_nova[3])
    elif figura_nova[0] == "Circulos":
        x1, y1 = figura_nova[1][0], figura_nova[1][1]
        x2, y2 = event.x, event.y

        lado = min(abs(x2 - x1), abs(y2 - y1))

        if x2 < x1:
            x2 = x1 - lado
        else:
            x2 = x1 + lado

        if y2 < y1:
            y2 = y1 - lado
        else:
            y2 = y1 + lado

        figura_nova = ("Circulos", (x1, y1, x2, y2), figura_nova[2], figura_nova[3])
    else : # figura_nova[0] == "linha"
        figura_nova = ("linha", (figura_nova[1][0], figura_nova[1][1], event.x, event.y), figura_nova[2], figura_nova[3])
    desenhar_figuras()
    desenhar_figura_nova()

# Quando mouse é solto
def incluir_figura_nova(event): 
    if not incompleta(figura_nova): # para evitar incluir figuras incompletas, como uma linha sem comprimento ou um rabisco com um único ponto
        figuras.append(figura_nova) 
    desenhar_figuras()

def desenhar_figuras():
    canvas.delete("all")
    for fig, values, cor, cor_preench in figuras:
        if fig == "linha":
            canvas.create_line(values[0], values[1], values[2], values[3], fill=cor)
        elif fig == 'Retangulos':
            canvas.create_rectangle(values[0], values[1], values[2], values[3], outline=cor, fill= cor_preench)
        elif fig == 'Ovais':
            canvas.create_oval(values[0], values[1], values[2], values[3], outline=cor, fill= cor_preench)
        elif fig == "Circulos":
            canvas.create_oval(values[0], values[1], values[2], values[3], outline=cor, fill= cor_preench)
        else : # fig == "rabisco"
            canvas.create_line(values,fill=cor)

def desenhar_figura_nova():
    fig, values, cor, cor_preench = figura_nova
    if fig == "linha":
        canvas.create_line(values[0], values[1], values[2], values[3], fill=cor,  dash=(4, 2))
    elif fig == 'Retangulos':
            canvas.create_rectangle(values[0], values[1], values[2], values[3], outline=cor, fill= cor_preench , dash=(4, 2))
    elif fig == 'Ovais':
            canvas.create_oval(values[0], values[1], values[2], values[3], outline=cor, fill= cor_preench, dash=(4, 2))
    elif fig == "Circulos":
            canvas.create_oval(values[0], values[1], values[2], values[3], outline=cor, fill= cor_preench, dash=(4, 2))
    else : # fig == "rabisco"
        canvas.create_line(values, fill=cor, dash=(4, 2))

def incompleta(figura):
    fig, values, cor, cor_preench = figura
    if fig == "linha":
        return (values[0], values[1]) == (values[2], values[3])
    else : # fig == "rabisco"
        return len(values) <= 1




#******* MAIN *******#

figuras = []       # Todas as figuras desenhadas
figura_nova = None # Figura que está sendo desenhada, mas ainda não foi incluída em figuras

root = Tk()
root.title('Exemplo de aplicação')
frame = Frame(root)

# Widgets arranjados com Layout grid dentro de frame
paddings = {'padx': 5, 'pady': 5} 

# label
label = ttk.Label(frame,  text='Escolha a forma do desenho:')
label.grid(column=0, row=0, sticky=W, **paddings)
label_cor = ttk.Label(frame, text='Cor da borda:')
label_cor.grid(column=0, row=1, sticky=W, **paddings)
label_preenchi = ttk.Label(frame, text='Cor de Preenchimento:')
label_preenchi.grid(column=0, row=2, sticky=W, **paddings)

# option menu
tipo_figura_var = StringVar(root) # Guarda o tipo de figura selecionado no option menu (linha ou rabisco)
option_menu = ttk.OptionMenu(frame, tipo_figura_var,
                             'Linha', 'Linha', 'Rabisco','Retangulos', 'Ovais', 'Circulos')
option_menu.grid(column=1, row=0, sticky=W, **paddings)

cor_borda_var = StringVar(root)
option_cor = ttk.OptionMenu(
    frame,
    cor_borda_var,
    'black',
    'black',
    'red',
    'blue',
    'green',
    'orange',
    'purple'
)
option_cor.grid(column=1, row=1, sticky=W, **paddings)

cor_preench_var = StringVar(root)

option_corP = ttk.OptionMenu(
    frame,
    cor_preench_var,
    '',
    '',
    'black',
    'white',
    'red',
    'blue',
    'green',
    'orange',
    'purple'
)
option_corP.grid(column=1, row=2, sticky=W, **paddings)

# Área de desenho
canvas = Canvas(frame, bg='white', width=600, height=600)
canvas.grid(column=0, row=3, columnspan=2, sticky=W, **paddings)

frame.pack()

# Eventos de mouse associados ao canvas - com seus callbacks
canvas.bind('<ButtonPress-1>', iniciar_figura_nova)
canvas.bind('<B1-Motion>', atualizar_figura_nova)
canvas.bind('<ButtonRelease-1>', incluir_figura_nova)

root.mainloop()
