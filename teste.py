from abc import ABC, abstractmethod
from tkinter import *
from tkinter import ttk

class Figura(ABC):
    def __init__(self, cor, cor_preench = ''):
        self.cor = cor
        self.cor_preench = cor_preench
    @abstractmethod
    def atualizar(self, x, y):
        pass
    @abstractmethod
    def desenhar(self, canvas):
        pass
    @abstractmethod
    def desenhar_nova(self, canvas):
        pass
    @abstractmethod
    def incompleta(self):
        return False

class Linha(Figura):
    def __init__(self, x1, y1, cor, cor_preench=''):
        super().__init__(cor, cor_preench)
        self.x1 = x1
        self.y1 = y1
        self.x2 = x1
        self.y2 = y1
    def atualizar(self, x, y):
        self.x2 = x
        self.y2 = y
    def desenhar(self, canvas):
        canvas.create_line(self.x1, self.y1, self.x2, self.y2, fill=self.cor)
    def desenhar_nova(self, canvas):
        canvas.create_line(self.x1, self.y1, self.x2, self.y2, fill=self.cor, dash=(4, 2))
    def incompleta(self):
        return self.x1 == self.x2 and self.y1 == self.y2

class Rabisco(Figura):
    def __init__(self, x1, y1, cor):
        super().__init__(cor)
        self.pontos = [(x1, y1)]
    def atualizar(self, x, y):
        self.pontos.append((x, y))
    def desenhar(self, canvas):
        canvas.create_line(self.pontos, fill=self.cor)
    def desenhar_nova(self, canvas):
         canvas.create_line(self.pontos, fill=self.cor, dash=(4, 2))
    def incompleta(self):
        return len(self.pontos) <= 1

class Retangulos(Linha):
    def __init__(self, x1, y1, cor, cor_preench):
        super().__init__(x1, y1, cor, cor_preench)
    def desenhar(self, canvas):
        canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2, outline=self.cor, fill=self.cor_preench)
    def desenhar_nova(self, canvas):
        canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2, outline=self.cor, fill=self.cor_preench, dash=(4, 2))

class Ovais(Linha):
    def __init__(self, x1, y1, cor, cor_preench):
        super().__init__(x1, y1, cor, cor_preench)
    def desenhar(self, canvas):
        canvas.create_oval(self.x1, self.y1, self.x2, self.y2, outline=self.cor, fill=self.cor_preench)
    def desenhar_nova(self, canvas):
        canvas.create_oval(self.x1, self.y1, self.x2, self.y2, outline=self.cor, fill=self.cor_preench, dash=(4, 2))

class Circulos(Ovais):
    def __init__(self, x1, y1, cor, cor_preench):
        super().__init__(x1, y1, cor, cor_preench)
    def atualizar(self, x, y):

        lado = min(abs(x - self.x1), abs(y - self.y1))

        if x >= self.x1:
            self.x2 = self.x1 + lado
        else:
            self.x2 = self.x1 - lado

        if y >= self.y1:
            self.y2 = self.y1 + lado
        else:
            self.y2 = self.y1 - lado

def iniciar_figura_nova(event):
    global figura_nova
    cor = cor_borda_var.get()
    preench = cor_preench_var.get()
    if tipo_figura_var.get() == "Linha":
        figura_nova = Linha(event.x, event.y, cor)
    elif tipo_figura_var.get() == "Rabisco":
        figura_nova = Rabisco(event.x, event.y, cor)
    elif tipo_figura_var.get() == "Retangulos":
        figura_nova = Retangulos(event.x, event.y, cor, preench)
    elif tipo_figura_var.get() == "Ovais":
        figura_nova = Ovais(event.x, event.y, cor, preench)
    else:
        figura_nova = Circulos(event.x, event.y, cor, preench)
def atualizar_figura_nova(event):
    global figura_nova
    if figura_nova is None:
        return
    figura_nova.atualizar(event.x, event.y)
    desenhar_figuras()
    figura_nova.desenhar_nova(canvas)
def incluir_figura_nova(event):
    global figura_nova
    if figura_nova is None:
        return
    if not figura_nova.incompleta():
        figuras.append(figura_nova)
    figura_nova = None
    desenhar_figuras()
def desenhar_figuras():
    canvas.delete("all")
    for figura in figuras:
        figura.desenhar(canvas)
    if figura_nova is not None:
        figura_nova.desenhar_nova(canvas)
    
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
