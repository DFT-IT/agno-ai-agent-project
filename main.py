# Imports
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.openai import OpenAIResponses
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.arxiv import ArxivTools
from agno.tools.yfinance import YFinanceTools
from agno.tools.hackernews import HackerNewsTools
from agno.team import Team
from agno.os import AgentOS

# Laden der Umgebungsvariablen
load_dotenv()

db = SqliteDb(db_file="tmp/team.db")

# === Agenten erstellen ===

news_agent = Agent(
    name="News Agent",
    role="Du findest aktuelle Tech-News auf HackerNews.",
    model=OpenAIResponses(id="gpt-4o-mini"),
    tools=[HackerNewsTools()],
    instructions=["Finde aktuelle News und fasse sie zusammen."],
)

research_agent = Agent(
    name="Research Agent",
    role="Du recherchierst akademische Paper auf arXiv.",
    model=OpenAIResponses(id="gpt-4o-mini"),
    tools=[ArxivTools()],
    instructions=["Suche nach relevanten akademischen Papern und fasse die Ergebnisse zusammen."],
)

stock_agent = Agent(
    name="Stock Agent",
    role="Du analysierst Aktienkurse und Finanzdaten.",
    model=OpenAIResponses(id="gpt-4o-mini"),
    tools=[YFinanceTools()],
    instructions=["Liefere aktuelle Aktienkurse, Analysten-Empfehlungen und Finanzdaten."],
)

web_agent = Agent(
    name="Web Search Agent",
    role="Du durchsuchst das Web nach aktuellen Informationen.",
    model=OpenAIResponses(id="gpt-4o-mini"),
    tools=[DuckDuckGoTools()],
    instructions=["Suche im Web nach relevanten Informationen."],
)

# === Team erstellen ===

team = Team(
    id="research-team",
    name="Research Team",
    mode="coordinate",
    model=OpenAIResponses(id="gpt-4o-mini"),
    members=[news_agent, research_agent, stock_agent, web_agent],
    instructions=[
        "Du bist ein Koordinator, der Anfragen an die passenden Team-Mitglieder delegiert.",
        "Nutze den News Agent für aktuelle Tech-News.",
        "Nutze den Research Agent für akademische Recherchen.",
        "Nutze den Stock Agent für Aktien- und Finanzdaten.",
        "Nutze den Web Search Agent für allgemeine Websuchen.",
        "Fasse die Ergebnisse aller beteiligten Agenten zusammen.",
    ],
    db=db,
    add_history_to_context=True,
    num_history_runs=5,
    store_member_responses=True,
    share_member_interactions=True,
    markdown=True,
)

# === Custom FastAPI App ===

custom_app = FastAPI(title="Research Team API")

class ChatRequest(BaseModel):
    message: str
    session_id: str | None = None

class AgentInfo(BaseModel):
    name: str
    role: str
    content: str

class ChatResponse(BaseModel):
    response: str
    session_id: Optional[str]
    agents_used: List[AgentInfo]

@custom_app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    response = team.run(request.message, session_id=request.session_id)

    # Beteiligte Agenten aus member_responses extrahieren
    agents_used = []
    if response.member_responses:
        for member_response in response.member_responses:
            agent_name = getattr(member_response, "agent_id", None) or "Unknown"
            agents_used.append(AgentInfo(
                name=agent_name,
                role="Team Member",
                content=member_response.content or "",
            ))

    return ChatResponse(
        response=response.content,
        session_id=response.session_id,
        agents_used=agents_used,
    )

# === AgentOS mit Custom App ===

agent_os = AgentOS(
    agents=[news_agent, research_agent, stock_agent, web_agent],
    teams=[team],
    base_app=custom_app,
)

app = agent_os.get_app()

if __name__ == "__main__":
    agent_os.serve(app="main:app", reload=True)