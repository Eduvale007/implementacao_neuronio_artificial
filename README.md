# Bot Clima + WhatsApp

Um aplicativo em Python que envia previsões do clima via WhatsApp usando **Tkinter**, **OpenWeatherMap API** e um neurônio simples para calcular a chance de ser um bom dia para sair.  

---

## Funcionalidades

- Consulta de clima em qualquer cidade, estado e país.
- Exibe temperatura, umidade e condição do clima.
- Calcula a probabilidade de ser bom para sair usando um **neurônio artificial simples**.
- Envia mensagens programadas pelo **WhatsApp** automaticamente.
- Interface gráfica simples com **Tkinter**.

---

## Tecnologias Utilizadas

- Python 3.x  
- Tkinter (GUI)  
- NumPy (cálculos do neurônio)  
- Requests (requisições à API OpenWeatherMap)  
- PyWhatKit (envio de mensagens via WhatsApp)  
- Dotenv (variáveis de ambiente)  

---

## Como funciona

- O script normaliza a temperatura e umidade e usa um neurônio simples para calcular a chance de ser bom para sair.

- A mensagem enviada contém:

- Localização

- Temperatura

- Umidade

- Condição do clima

- Probabilidade de sair

- Recomendação final

---

## Exemplo de mensagem

-Exemplo de Mensagem
📍 São Paulo - SP (BR)
🌡 Temp: 28°C
💧 Umidade: 65%
☁ Clima: céu limpo
🔎 Chance de ser bom para sair: 72.3%
✅ Pode sair tranquilo!

## Instalação

1. Clone este repositório:

```bash
git clone https://github.com/seu-usuario/bot-clima-whatsapp.git
cd bot-clima-whatsapp

Crie e ative um ambiente virtual (opcional, mas recomendado):

python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows


Instale as dependências:

pip install -r requirements.txt


Crie um arquivo .env com sua API_KEY do OpenWeatherMap:

API_KEY=SEU_API_KEY_AQUI

Uso

Execute o script:

python bot_clima.py


Preencha os campos:

Número do WhatsApp (ex: +5511999999999)

Cidade

Estado (sigla)

País (sigla)

Clique em Enviar.
O bot enviará a mensagem programada com as informações do clima e a probabilidade de ser um bom dia para sair.
