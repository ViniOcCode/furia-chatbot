# Panterinha | o ChatBot da FURIA

![GitHub repo size](https://img.shields.io/github/repo-size/iuricode/README-template?style=for-the-badge)
![GitHub language count](https://img.shields.io/github/languages/count/iuricode/README-template?style=for-the-badge)
![GitHub forks](https://img.shields.io/github/forks/iuricode/README-template?style=for-the-badge)
![Bitbucket open issues](https://img.shields.io/bitbucket/issues/iuricode/README-template?style=for-the-badge)
![Bitbucket open pull requests](https://img.shields.io/bitbucket/pr-raw/iuricode/README-template?style=for-the-badge)

<img src="imagem.png" alt="Exemplo imagem">

> Um chatbot focado para os fãs de CS da FURIA! Focado em prover informações rápido e fácil!

### Ajustes e melhorias

O projeto ainda está em desenvolvimento e as próximas atualizações serão voltadas para as seguintes tarefas:

- [ ] Integrar WebSocket para dados de jogos ao vivo
- [ ] Melhorar o sistema de detecção de intenção usando NLP (tipo spaCy ou transformers).
- [ ] Implementar cache para diminuir requisições desnecessárias.
- [ ] Criar API REST para usar o bot em frontends.

## 💻 Pré-requisitos

Antes de começar, verifique se você atendeu aos seguintes requisitos:

- Você instalou a versão mais recente de 
 - Python 3.x e instalou os requerimentos usando `pip install requeriments.txt`
- Você leu como o projeto na [seção](#como-funciona-o-ChatBot-da-FURIA)

## 🚀 instalando o ChatBot da Furia

Se você quiser instalar o código fonte para depuarar em seu ambiente basta você fazer

```bash
git clone https://github.com/ViniOcCode/furia-chatbot.git
```

## ☕ Usando o ChatBot da Furia

Para usar O ChatBot da Furia, você pode perguntar sobre:
 - 🤖 Quem criou o bot
 - 🎲 Curiosidade aleatória
 - 🐱‍👤 Sobre a FURIA
 - 📺 Onde assistir as transmissões?
 - 📊 Resultados recentes (Time principal e time feminino)
 - 🥇 Ranqueamento global e nacional (Time principal e time feminino)
 - 🎯 Próximo jogo (Time principal e time feminino)
 - 📅 Próximos eventos (Time principal e time feminino)
 - 🧑‍🤝‍🧑 Elenco atual (Time principal e time feminino)

## 📫 Contribuindo para o ChatBot da FURIA

Para contribuir com o ChatBot da FURIA siga estas etapas:

1. Bifurque este repositório.
2. Crie um branch: `git checkout -b <nome_branch>`.
3. Faça suas alterações e confirme-as: `git commit -m '<mensagem_commit>'`
4. Envie para o branch original: `git push origin <nome_do_projeto> / <local>`
5. Crie a solicitação de pull.

Como alternativa, consulte a documentação do GitHub em [como criar uma solicitação pull](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request).

---

## 🧠 Como funciona o ChatBot da FURIA

O ChatBot é dividido em módulos especializados que interpretam mensagens e retornam respostas com base no conteúdo.

## 🔁 Fluxo de mensagem

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
│   ├── models/
│   │   ├── __init__.py
│   │   ├── chatresponses.py       # Lógica para identificar intenção e gerar resposta
│   │   ├── events.py              # Eventos futuros da FURIA
│   │   ├── lineup.py              # Elenco atual (time principal e feminino)
│   │   ├── matches.py             # Últimos e próximos jogos
│   │   ├── ranking.py             # Ranking nacional e internacional
│   │   └── utils.py               # Palavras-chave e dados estáticos
│
├── static/                        # Arquivos estáticos para o frontend
│   ├── bot-icon.png
│   ├── user-icon.png
│   ├── script.js                  # JS que envia a mensagem do usuário via fetch
│   └── styles.css                 # Estilos do chat no frontend
│
├── templates/
│   └── __init__.py (vazio ou não usado)
│   └── index.html                 # Página HTML do chatbot
│
├── main.py                        # Cria a app Flask e registra as rotas
├── requirements.txt               # Dependências do projeto
├── .gitignore
└── README.md
``` 
## 📝 Licença

Esse projeto está sob licença. Veja o arquivo [LICENÇA](LICENSE.md) para mais detalhes.
