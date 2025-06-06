# Panterinha | o ChatBot da FURIA

<img src="app/static/bot-icon.png" alt="Panterinha">

> Um chatbot focado para os fãs de CS da FURIA! Focado em prover informações rápido e fácil!

### Ajustes e melhorias

O projeto é um protótipo e as melhorias possíveis seriam:

- [ ] Integrar WebSocket para dados de jogos ao vivo
- [ ] Melhorar o sistema de detecção de intenção usando NLP (tipo spaCy ou transformers).
- [ ] Implementar cache para diminuir requisições desnecessárias.
- [ ] Criar API REST para usar o bot em frontends.
- [ ] Em vez de respostas predefinidas, usar uma LLM para respostas mais orgânicas.

## 💻 Pré-requisitos

Antes de começar, verifique se você atendeu aos seguintes requisitos:

- Python 3.13 e instalou os requerimentos usando 
```bash
pip install requirements.txt
```
- Você leu como o projeto [funciona](#como-funciona-a-aplicação)
- OU para você pular todos esses passos, você pode baixar Docker e dar uma olhada [aqui](README.docker.md)


## 🚀 instalando a aplicação

Se você quiser instalar o código fonte para depuarar em seu ambiente basta você fazer

```bash
git clone https://github.com/ViniOcCode/furia-chatbot.git
```

## ☕ Usando a aplicação

Você pode perguntar para a Panterinha sobre:
 - 🤖 Quem criou o bot
 - 🎲 Curiosidade aleatória
 - 🐱‍👤 Sobre a FURIA
 - 📺 Onde assistir as transmissões?
 - 📊 Resultados recentes (Time principal e time feminino)
 - 🥇 Ranqueamento global e nacional (Time principal e time feminino)
 - 🎯 Próximo jogo (Time principal e time feminino)
 - 📅 Próximos eventos (Time principal e time feminino)
 - 🧑‍🤝‍🧑 Elenco atual (Time principal e time feminino)

## 📫 Contribuindo para a aplicação

Para contribuir com a aplicação da FURIA siga estas etapas:

1. Bifurque este repositório.
2. Crie um branch: `git checkout -b <nome_branch>`.
3. Faça suas alterações e confirme-as: `git commit -m '<mensagem_commit>'`
4. Envie para o branch original: `git push origin <nome_do_projeto> / <local>`
5. Crie a solicitação de pull.

Como alternativa, consulte a documentação do GitHub em [como criar uma solicitação pull](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request).

---

## Como funciona a aplicação

O ChatBot é dividido em módulos especializados que interpretam mensagens e retornam respostas com base no conteúdo.

## 🔁 Fluxo da aplicação 

1. Usuário envia mensagem via frontend (form no `index.html`)
2. `script.js` faz `fetch('/chat')` com o texto do usuário
3. `controllers/chat.py` recebe o POST e envia para `chatresponses.py`
4. A função analisa a intenção usando palavras-chave (com `RapidFuzz`)
5. Se necessário, busca dados em `lineup.py`, `matches.py`, `ranking.py`, etc.
6. Retorna a resposta formatada ao frontend

---

### 📁 Estrutura do Projeto
```
FURIA-CHATBOT/
│
├── app/
│   ├── controllers/
│   │   └── chat.py                # Rota que recebe a mensagem do usuário e retorna a resposta
│   │
│   └── models/
│      ├── chatresponses.py       # Lógica para identificar intenção e gerar resposta
│      ├── events.py              # Eventos futuros da FURIA
│      ├── lineup.py              # Elenco atual (time principal e feminino)
│      ├── matches.py             # Últimos e próximos jogos
│      ├── ranking.py             # Ranking nacional e internacional
│      └── utils.py               # Palavras-chave e dados estáticos
│
├── static/                        # Arquivos estáticos para o frontend
│   ├── bot-icon.png
│   ├── user-icon.png
│   ├── script.js                  # JS que envia a mensagem do usuário via fetch
│   └── styles.css                 # Estilos do chat no frontend
│
├── templates/
│   └── index.html                 # Página HTML do chatbot
│
├── main.py                        # Cria a app Flask e registra as rotas
├── requirements.txt               # Dependências do projeto
├── .gitignore
├── README.md
└── __init__.py                    # Configuração da aplicação Flask
``` 

## 📝 Licença
Esse projeto está sob licença. Veja o arquivo [LICENÇA](LICENSE) para mais detalhes.
