'''
import requests
import numpy as np
import pywhatkit as kit
import datetime
import tkinter as tk
from tkinter import messagebox

# ========= CONFIGURAÇÃO =========
API_KEY = "9116c359de85431d39e0ca9735467d0c"  # OpenWeatherMap

# Funções de ativação
def sigmoid(z):
    return 1 / (1 + np.exp(-z))

def dsigmoid(a):
    return a * (1 - a)

# Neurônio simples
class Neuron:
    def __init__(self, n_inputs, lr=0.1, seed=42):
        rng = np.random.default_rng(seed)
        self.w = rng.normal(0, 1, size=(n_inputs,)) * 0.1
        self.b = 0.0
        self.lr = lr

    def forward(self, x):
        return sigmoid(np.dot(self.w, x) + self.b)

    def train_step(self, x, y_true):
        a = self.forward(x)
        error = a - y_true
        grad = error * dsigmoid(a)
        self.w -= self.lr * grad * x
        self.b -= self.lr * grad

# ====== Dados de treino fictícios ======
X = np.array([
    [30, 40], [32, 50], [28, 60], [22, 30],
    [35, 35], [18, 50], [29, 45], [25, 80]
], dtype=float)
y = np.array([1, 1, 0, 0, 1, 0, 1, 0], dtype=float)

X[:,0] /= 40
X[:,1] /= 100

neuron = Neuron(n_inputs=2, lr=0.5)
for _ in range(2000):
    idx = np.random.permutation(len(X))
    for i in idx:
        neuron.train_step(X[i], y[i])

# ===== Função principal =====
def enviar_mensagem():
    numero = entry_numero.get().strip()
    cidade = entry_cidade.get().strip()

    # Remove espaços e traços
    numero = numero.replace(" ", "").replace("-", "")

    # Adiciona +55 se não tiver código internacional
    if not numero.startswith("+"):
        numero = "+55" + numero

    # Validação básica
    if len(numero) < 13:
        messagebox.showerror("Erro", "Número inválido! Exemplo: 11999999999 ou +5511999999999")
        return

    if not cidade:
        messagebox.showerror("Erro", "Digite a cidade!")
        return

    # pegar clima
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={API_KEY}&units=metric&lang=pt_br"
        res = requests.get(url)
        dados = res.json()
        temp = dados['main']['temp']
        umid = dados['main']['humidity']
        condicao = dados['weather'][0]['description']
    except:
        messagebox.showerror("Erro", "Não foi possível obter dados do clima.")
        return

    # neurônio calcula
    entrada = np.array([temp/40, umid/100])
    prob = neuron.forward(entrada)

    mensagem = (
        f"📍 {cidade}\n"
        f"🌡 Temp: {temp}°C\n"
        f"💧 Umidade: {umid}%\n"
        f"☁ Clima: {condicao}\n"
        f"🔎 Chance de ser bom para sair: {prob*100:.1f}%\n"
        + ("✅ Pode sair tranquilo!" if prob >= 0.5 else "🚫 Melhor ficar em casa...")
    )

    # agenda WhatsApp 2 minutos à frente
    agora = datetime.datetime.now()
    hora = agora.hour
    minuto = agora.minute + 2
    kit.sendwhatmsg(numero, mensagem, hora, minuto)
    messagebox.showinfo("Pronto", f"Mensagem agendada para {hora}:{minuto:02d}")


# ===== Interface Tkinter =====
root = tk.Tk()
root.title("Clima  WhatsApp")

tk.Label(root, text="Número do WhatsApp (+55DDDNUMERO):").grid(row=0, column=0, sticky="w")
entry_numero = tk.Entry(root, width=25)
entry_numero.grid(row=0, column=1)

tk.Label(root, text="Cidade:").grid(row=1, column=0, sticky="w")
entry_cidade = tk.Entry(root, width=25)
entry_cidade.grid(row=1, column=1)

btn_enviar = tk.Button(root, text="Enviar", command=enviar_mensagem)
btn_enviar.grid(row=2, column=0, columnspan=2, pady=10)

root.mainloop()
'''
import requests
import numpy as np
import pywhatkit as kit
import datetime
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk 

# ========= CONFIGURAÇÃO =========
API_KEY = "9116c359de85431d39e0ca9735467d0c"  # OpenWeatherMap

# Funções de ativação
def sigmoid(z):
    return 1 / (1 + np.exp(-z))

def dsigmoid(a):
    return a * (1 - a)

# Neurônio simples
class Neuron:
    def __init__(self, n_inputs, lr=0.1, seed=42):
        rng = np.random.default_rng(seed)
        self.w = rng.normal(0, 1, size=(n_inputs,)) * 0.1
        self.b = 0.0
        self.lr = lr

    def forward(self, x):
        return sigmoid(np.dot(self.w, x) + self.b)

    def train_step(self, x, y_true):
        a = self.forward(x)
        error = a - y_true
        grad = error * dsigmoid(a)
        self.w -= self.lr * grad * x
        self.b -= self.lr * grad

# ====== Dados de treino  ======
X = np.array([
    [30, 40], [32, 50], [28, 60], [22, 30],
    [35, 35], [18, 50], [29, 45], [25, 80],
    # Dados intermediários para suavizar previsões
    [15, 90], [20, 85], [16, 70], [18, 60], [23, 65], [24, 50]
], dtype=float)

y = np.array([
    1, 1, 0, 0, 1, 0, 1, 0,
    # Saídas intermediárias
    0.2, 0.3, 0.4, 0.5, 0.55, 0.6
], dtype=float)

# Normaliza
X[:,0] /= 40
X[:,1] /= 100

# Treina o neurônio
neuron = Neuron(n_inputs=2, lr=0.5)
for _ in range(2000):
    idx = np.random.permutation(len(X))
    for i in idx:
        neuron.train_step(X[i], y[i])

# ===== Função principal =====
def enviar_mensagem():
    numero = entry_numero.get().strip()
    cidade = entry_cidade.get().strip()
    estado = entry_estado.get().strip()
    pais = entry_pais.get().strip()

    numero = numero.replace(" ", "").replace("-", "")
    if not numero.startswith("+"):
        numero = "+55" + numero

    if len(numero) < 13:
        messagebox.showerror("Erro", "Número inválido! Exemplo: 11999999999 ou +5511999999999")
        return

    if not cidade or not estado or not pais:
        messagebox.showerror("Erro", "Preencha cidade, estado e país!")
        return

    local = f"{cidade},{estado},{pais}"

    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={local}&appid={API_KEY}&units=metric&lang=pt_br"
        res = requests.get(url)
        dados = res.json()

        if dados.get("cod") != 200:
            raise Exception(dados.get("message", "Erro desconhecido."))

        temp = dados['main']['temp']
        umid = dados['main']['humidity']
        condicao = dados['weather'][0]['description']
    except Exception as e:
        messagebox.showerror("Erro", f"Não foi possível obter dados do clima.\n{e}")
        return

    # Entrada para neurônio e probabilidade
    entrada = np.array([temp/40, umid/100])
    prob = neuron.forward(entrada)
    prob = max(prob, 0.1)  # Garante valor mínimo de 10%

    mensagem = (
        f"📍 {cidade} - {estado} ({pais})\n"
        f"🌡 Temp: {int(round(temp))}°C\n" 
        f"💧 Umidade: {umid}%\n"
        f"☁ Clima: {condicao}\n"
        f"🔎 Chance de ser bom para sair: {prob*100:.1f}%\n"
        + ("✅ Pode sair tranquilo!" if prob >= 0.5 else "🚫 Melhor ficar em casa...")
    )

    agora = datetime.datetime.now()
    hora = agora.hour
    minuto = agora.minute + 2
    kit.sendwhatmsg(numero, mensagem, hora, minuto)
    messagebox.showinfo("Pronto", f"Mensagem agendada para {hora}:{minuto:02d}")

# ===== Interface Tkinter =====
root = tk.Tk()
root.title("Bot Clima + WhatsApp")

try:
    img = Image.open("cerebro.png").resize((100,100))
    img_tk = ImageTk.PhotoImage(img)
    label_img = tk.Label(root, image=img_tk)
    label_img.grid(row=0, column=0, columnspan=2, pady=5)
except:
    pass

tk.Label(root, text="Número do WhatsApp (+55DDDNUMERO):").grid(row=1, column=0, sticky="w")
entry_numero = tk.Entry(root, width=25)
entry_numero.grid(row=1, column=1)

tk.Label(root, text="Cidade:").grid(row=2, column=0, sticky="w")
entry_cidade = tk.Entry(root, width=25)
entry_cidade.grid(row=2, column=1)

tk.Label(root, text="Estado (Sigla):").grid(row=3, column=0, sticky="w")
entry_estado = tk.Entry(root, width=25)
entry_estado.grid(row=3, column=1)

tk.Label(root, text="País (Sigla):").grid(row=4, column=0, sticky="w")
entry_pais = tk.Entry(root, width=25)
entry_pais.grid(row=4, column=1)

btn_enviar = tk.Button(root, text="Enviar", command=enviar_mensagem)
btn_enviar.grid(row=5, column=0, columnspan=2, pady=10)

root.mainloop()
