# Imports
from dotenv import load_dotenv
from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.openai import OpenAIResponses
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.arxiv import ArxivTools
import httpx
import json
from agno.tools import tool

# Laden der Umgebungsvariablen
load_dotenv()

@tool()
def get_top_hackernews_stories(num_stories: int = 5) -> str:
    """Fetch top stories from Hacker News.

    Args:
        num_stories (int): Number of stories to retrieve.
    """
    response = httpx.get("https://hacker-news.firebaseio.com/v0/topstories.json")
    story_ids = response.json()

    stories = []
    for story_id in story_ids[:num_stories]:
        story_response = httpx.get(
            f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
        )
        story = story_response.json()
        story.pop("text", None)
        stories.append(story)

    return json.dumps(stories)

def main():
	# Agent mit OpenAI Modell, Datenbank, Chat History und Tools erstellen
    agent = Agent(
        model=OpenAIResponses(id="gpt-4o-mini"),
        db=SqliteDb(db_file="tmp/agent.db"),
        tools=[DuckDuckGoTools(), ArxivTools(), get_top_hackernews_stories],
        instructions=["Du bist ein Tech-News Assistent. Nutze das HackerNews Tool um aktuelle Stories zu finden."],
        add_history_to_context=True,
        num_history_runs=5,
        markdown=True,
    )
    agent.cli_app(stream=True)

if __name__ == "__main__":
    main()