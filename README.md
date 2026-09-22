# Panterinha — FURIA Fan Chatbot

[![Tests](https://github.com/ViniOcCode/furia-chatbot/actions/workflows/tests.yml/badge.svg)](https://github.com/ViniOcCode/furia-chatbot/actions/workflows/tests.yml)

An unofficial Flask chatbot prototype for Counter-Strike fans. Panterinha combines fuzzy intent recognition with modular web-scraping adapters to answer questions about FURIA's teams, matches, events, rankings, and lineups.

<p align="center">
  <img src="app/static/bot-icon.png" alt="Panterinha chatbot icon" width="180">
</p>

> [!NOTE]
> This is an independent educational fan project. It is not affiliated with or endorsed by FURIA or HLTV. Live answers depend on third-party page structure and may become unavailable when those pages change.

## What it demonstrates

- A Flask JSON endpoint consumed by a browser chat interface.
- Accent-insensitive message normalization.
- Fuzzy keyword matching with RapidFuzz.
- Intent routing separated from response formatting.
- Team-context detection for the main and women's rosters.
- Modular parsers for matches, events, rankings, and lineups.
- Brazilian timezone conversion for match and event timestamps.
- Containerized execution with Docker and deployment configuration for Fly.io.
- Offline automated tests for HTTP routes, intent selection, team context, and HTML parsing.

## Supported questions

Panterinha recognizes questions about:

- Recent and upcoming matches.
- Main and women's lineups.
- Upcoming events.
- Global and Brazilian rankings.
- Where to watch matches.
- FURIA facts and official social links.

## Request flow

```text
Browser chat
    -> POST /chat
    -> normalize + fuzzy intent match
    -> select team context
    -> local response or scraping adapter
    -> formatted JSON response
```

Only intents that need changing information call the external adapters. Greetings, help, social links, and trivia are produced locally.

## Technology stack

- Python 3.13
- Flask
- RapidFuzz and Unidecode
- Beautiful Soup and Cloudscraper
- HTML, CSS, and JavaScript
- Gunicorn and Docker
- Pytest and GitHub Actions

## Running locally

```bash
git clone https://github.com/ViniOcCode/furia-chatbot.git
cd furia-chatbot
python -m venv .venv
```

Activate the environment:

```bash
# Linux/macOS
source .venv/bin/activate

# Windows PowerShell
.venv\Scripts\Activate.ps1
```

Install and start the development server:

```bash
pip install -r requirements.txt
python main.py
```

Open [http://localhost:5000](http://localhost:5000).

## Docker

```bash
docker build -t furia-chatbot:1.0 .
docker run --rm -p 8080:5000 furia-chatbot:1.0
```

Open [http://localhost:8080](http://localhost:8080). Additional container commands are documented in [README.docker.md](README.docker.md).

## Tests

```bash
pip install -r requirements-dev.txt
pytest -q
```

The tests intentionally use controlled HTML fixtures rather than contacting HLTV, making the CI suite deterministic and respectful of the external service.

## Project structure

```text
app/
  controllers/chat.py       Flask routes
  models/chatresponses.py   Intent routing and response formatting
  models/matches.py         Match parser
  models/events.py          Event parser
  models/lineup.py          Roster parser
  models/ranking.py         Ranking parser
  models/utils.py           Keywords, teams, dates, and shared HTTP client
  static/                   Browser UI assets
  templates/                Chat page
tests/                      Offline behavior and parser tests
main.py                     Application entry point
```

## Limitations

- The chatbot uses fuzzy keyword routing rather than a trained language model.
- Scraping adapters are coupled to third-party HTML and require maintenance when markup changes.
- Some static trivia and ranking routes reflect the project's original 2025 prototype period.
- Responses are informational and should be checked against official sources for current competitive data.

## License

[MIT](LICENSE)

<details>
<summary><strong>Português</strong></summary>

## Sobre o projeto

Panterinha é um protótipo não oficial de chatbot para fãs de Counter-Strike. A aplicação usa Flask, reconhecimento aproximado de intenções e módulos de scraping para responder perguntas sobre partidas, eventos, rankings e escalações da FURIA.

Este é um projeto educacional independente, sem afiliação ou endosso da FURIA ou da HLTV. Respostas dinâmicas dependem da estrutura de páginas externas e podem deixar de funcionar quando essas páginas mudam.

### O que o projeto demonstra

- API Flask consumida pela interface de chat.
- Normalização de mensagens e reconhecimento de intenção com RapidFuzz.
- Detecção de contexto entre os times principal e feminino.
- Parsers separados para partidas, eventos, rankings e escalações.
- Conversão de datas para o fuso brasileiro.
- Docker, configuração de deploy e testes automatizados sem acesso à rede.

### Execução

Crie um ambiente virtual, instale `requirements.txt`, execute `python main.py` e acesse [http://localhost:5000](http://localhost:5000).

Para executar os testes, instale `requirements-dev.txt` e rode `pytest -q`.

</details>
