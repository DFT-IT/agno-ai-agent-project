# Imports
from dotenv import load_dotenv
from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.openai import OpenAIResponses
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.arxiv import ArxivTools

# Laden der Umgebungsvariablen
load_dotenv()

def main():
	# Agent mit OpenAI Modell, Datenbank, Chat History und Tools erstellen
    agent = Agent(
        model=OpenAIResponses(id="gpt-4o-mini"),
        db=SqliteDb(db_file="tmp/agent.db"),
        tools=[DuckDuckGoTools(), ArxivTools()],
        instructions=[
            "Du bist ein Forschungsassistent.",
            "Nutze ArxivTools um akademische Paper zu suchen und zusammenzufassen oder DuckDuckGo zum Suchen.",
        ],
        add_history_to_context=True,
        num_history_runs=5,
        markdown=True,
    )
    agent.cli_app(stream=True)

if __name__ == "__main__":
    main()