import os

from dotenv import load_dotenv
from openai import OpenAI

# Umgebungsvariablen aus der .env-Datei laden
load_dotenv()

# OpenAI-Client erstellen und das ausgewählte Modell auslesen
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
model = os.getenv("OPENAI_MODEL", "gpt-5-mini")

# Prompt an das Modell senden
response = client.responses.create(
    model=model,
    input="Erkläre in einem Satz, was ein Large Language Model ist.",
)

# Generierte Antwort ausgeben
print(response.output_text)
