# Imports
from dotenv import load_dotenv
from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.openai import OpenAIResponses

# Laden der Umgebungsvariablen
load_dotenv()

def main():
    # Agent mit OpenAI Modell, Datenbank und Chat History erstellen
    agent = Agent(
        model=OpenAIResponses(id="gpt-4o-mini"),
        db=SqliteDb(db_file="tmp/agent.db"),
        add_history_to_context=True,
        num_history_runs=5,
        markdown=True,
    )

    # Interaktive CLI starten
    agent.cli_app(stream=True)

if __name__ == "__main__":
    main()