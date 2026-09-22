import pytest

from app import create_app
from app.models.chatresponses import detect_team, match_intent
from app.models.matches import matches


@pytest.fixture
def client():
    app = create_app()
    app.config.update(TESTING=True)
    return app.test_client()


def test_home_page_loads(client):
    response = client.get("/")

    assert response.status_code == 200
    assert b"Panterinha" in response.data


def test_chat_returns_a_local_greeting_without_scraping(client):
    response = client.post("/chat", json={"message": "oi"})

    assert response.status_code == 200
    assert "response" in response.get_json()
    assert "FURIA" in response.get_json()["response"]


def test_intent_and_team_detection():
    assert match_intent("qual o proximo jogo?") == "proximo_jogo"
    assert detect_team("qual o elenco feminino?")["name"] == "FURIA Fe"


def test_match_rows_are_parsed_from_controlled_html():
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(
        """
        <table>
          <tr class="event-header-cell"><a class="a-reset">Test Cup</a></tr>
          <tr class="team-row">
            <td class="date-cell"><span data-unix="1746403200000"></span></td>
            <td><a class="team-2" href="/team/1/example">Example</a></td>
            <td><a class="matchpage-button" href="/matches/1/test"></a></td>
            <td><div class="score-cell">13:7</div></td>
          </tr>
        </table>
        """,
        "html.parser",
    )

    result = matches(soup.find_all("tr"))

    assert result == [
        {
            "event": "Test Cup",
            "date": "04/05 às 21h",
            "enemy": "Example",
            "livestreams": "https://www.hltv.org//matches/1/test",
            "score": "#GOFURIA 13x7 <a href='https://www.hltv.org//team/1/example' target='_blank'>Example</a>",
        }
    ]
