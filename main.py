# Imports
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.openai import OpenAIResponses
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.arxiv import ArxivTools
from agno.os import AgentOS
from agno.tools import tool
import httpx
import json

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

# Agent erstellen
agent = Agent(
    id="tech-agent",
    model=OpenAIResponses(id="gpt-4o-mini"),
    db=SqliteDb(db_file="tmp/agent.db"),
    tools=[DuckDuckGoTools(), ArxivTools(), get_top_hackernews_stories],
    instructions=["Du bist ein Tech-News Assistent. Nutze das HackerNews Tool um aktuelle Stories zu finden."],
    add_history_to_context=True,
    num_history_runs=5,
    markdown=True,
)

# Custom FastAPI App
custom_app = FastAPI(title="Tech Agent API")

# Request Schema
class ChatRequest(BaseModel):
    message: str
    session_id: str | None = None

# Sauberer Chat Endpoint
@custom_app.post("/chat")
def chat(request: ChatRequest):
    response = agent.run(request.message, session_id=request.session_id)
    return {
        "response": response.content,
        "session_id": response.session_id,
    }

# AgentOS mit Custom App als base_app
agent_os = AgentOS(
    agents=[agent],
    base_app=custom_app,
)

app = agent_os.get_app()

if __name__ == "__main__":
    agent_os.serve(app="main:app", reload=True)