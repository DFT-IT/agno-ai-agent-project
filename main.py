# Imports
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.openai import OpenAIResponses

# Laden der Umgebungsvariablen
load_dotenv()

def main():
    # Agent mit OpenAI Modell erstellen
    agent = Agent(
        model=OpenAIResponses(id="gpt-4o-mini"),
        markdown=True,
    )
    # Anfrage an Agent senden und Antwort ausgeben
    agent.print_response("Tell me a very funny software engineering joke", stream=True)

if __name__ == "__main__":
    main()