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
    numero = entry_numero.get()
    cidade = entry_cidade.get()
    if not numero or not cidade:
        messagebox.showerror("Erro", "Preencha todos os campos!")
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
root.title("Bot Clima + WhatsApp")

tk.Label(root, text="Número do WhatsApp (+55DDDNUMERO):").grid(row=0, column=0, sticky="w")
entry_numero = tk.Entry(root, width=25)
entry_numero.grid(row=0, column=1)

tk.Label(root, text="Cidade:").grid(row=1, column=0, sticky="w")
entry_cidade = tk.Entry(root, width=25)
entry_cidade.grid(row=1, column=1)

btn_enviar = tk.Button(root, text="Enviar", command=enviar_mensagem)
btn_enviar.grid(row=2, column=0, columnspan=2, pady=10)

root.mainloop()
