# AI Agents with Python

Beispielprojekt fuer einen AI-Agent-Stack mit Python:

- `agent`: LangChain-Agent mit OpenAI-GPT-Modell und FastAPI-Endpunkt
- `mcp`: FastMCP-Server, der Beispieldaten aus DuckDB als Tools bereitstellt
- `app`: Streamlit-Frontend mit Chat-Interface fuer den Agenten
- `scripts`: Skripte zum Generieren der CSV-Beispieldaten und Laden nach DuckDB

## Projektstruktur

```text
.
├── agent/
│   ├── main.py
│   ├── requirements.txt
│   ├── service.py
│   └── mcp_client.py
├── app/
│   ├── requirements.txt
│   └── streamlit_app.py
├── data/
│   ├── raw/
│   └── warehouse/
├── mcp/
│   ├── requirements.txt
│   ├── server.py
│   └── db.py
├── scripts/
│   ├── generate_sample_data.py
│   └── load_duckdb.py
├── .env.example
└── pyproject.toml
```

## Architektur

1. `scripts/generate_sample_data.py` erzeugt eine CSV mit Demo-Bestelldaten.
2. `scripts/load_duckdb.py` laedt die CSV in eine lokale DuckDB-Datei.
3. Der FastMCP-Server kapselt SQL-Abfragen auf DuckDB als MCP-Tools.
4. Der FastAPI-Agent nutzt LangChain und ruft bei Datenfragen die MCP-Tools auf.
5. Das Streamlit-Frontend spricht nur mit dem FastAPI-Agenten.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
cp .env.example .env
```

Danach `OPENAI_API_KEY` in `.env` setzen.

## Service-Abhaengigkeiten

Agent-Service:

```bash
pip install -r agent/requirements.txt
```

MCP-Service:

```bash
pip install -r mcp/requirements.txt
```

Streamlit-App:

```bash
pip install -r app/requirements.txt
```

Optional kannst du alternativ weiterhin alle Abhaengigkeiten gesammelt ueber `pip install -e .` installieren.

## Daten vorbereiten

```bash
python scripts/generate_sample_data.py
python scripts/load_duckdb.py
```

## Dienste starten

MCP-Server:

```bash
python mcp/server.py
```

Agent API:

```bash
uvicorn agent.main:app --reload --port 8000
```

Streamlit-App:

```bash
streamlit run app/streamlit_app.py
```

## Beispiel-URLs

- Agent API: `http://localhost:8000`
- MCP Server: `http://localhost:9000/mcp`
- Streamlit: `http://localhost:8501`

## Hinweise

- Die Projektteile sind klar getrennt in `agent/`, `mcp/` und `app/`, ohne `src`-Layout.
- Die CSV wird unter `data/raw/` erzeugt, die DuckDB unter `data/warehouse/` abgelegt.
- Fuer haeufige Aufgaben kannst du auch `make install`, `make data`, `make mcp`, `make agent` und `make app` nutzen.
