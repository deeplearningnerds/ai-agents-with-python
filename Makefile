PYTHON ?= python3

.PHONY: install data mcp agent app

install:
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -e .

data:
	$(PYTHON) scripts/generate_sample_data.py
	$(PYTHON) scripts/load_duckdb.py

mcp:
	$(PYTHON) mcp/server.py

agent:
	uvicorn agent.main:app --reload --port 8000

app:
	streamlit run app/streamlit_app.py
