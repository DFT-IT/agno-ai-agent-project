# 🤖 AI Agent Project mit Agno Framework

Ein praktisches Demonstrationsprojekt zum Erlernen von **AI Agents** anhand des **Agno Frameworks**. 

## 📋 Übersicht

Dieses Projekt zeigt, wie man mit Python und dem Agno Framework intelligente, spezialisierte AI-Agenten erstellt, die zusammenarbeiten, um komplexe Aufgaben zu lösen. 

### Was ist enthalten?

- **Research Team**: Ein Team aus mehreren spezialisierten Agenten
  - 📰 **News Agent**: Sammelt aktuelle Tech-News von HackerNews
  - 🔬 **Research Agent**: Sucht und analysiert akademische Paper auf arXiv
  - 📈 **Stock Agent**: Liefert Aktienkurse und Finanzdaten
  - 🌐 **Web Search Agent**: Durchsucht das Web mit DuckDuckGo

- **FastAPI Backend**: REST API für Agent-Kommunikation
- **Streamlit Frontend**: Benutzerfreundliche Weboberfläche mit Text- und Voice-Input
  - 💬 Text-basierte Eingabe
  - 🎤 Sprach-basierte Eingabe (mit Whisper-Transkription)
  - 🔊 Text-zu-Sprache Output

## 🎯 Lernziele

Dieses Projekt vermittelt folgende Konzepte:
- Grundlagen von AI Agents und deren Einsatz
- Agent-Rollen und spezialisierte Aufgaben
- Team-Koordination zwischen mehreren Agenten
- Integration mit OpenAI-Modellen
- Tool-Integration (DuckDuckGo, arXiv, Yahoo Finance, HackerNews)
- FastAPI und Streamlit für AI-Anwendungen
- Persistente Speicherung von Agent-Interaktionen

## 🚀 Installation

### Voraussetzungen
- Python 3.13+
- [uv](https://github.com/astral-sh/uv) (schneller Python Package Manager)
- OpenAI API Key
- Git

### Schritt-für-Schritt Anleitung

1. **Repository klonen:**
```bash
git clone https://github.com/DFT-IT/agno-ai-agent-project.git
cd agno-ai-agent-project
```

2. **Dependencies installieren mit uv:**
```bash
uv sync
```

3. **.env Datei erstellen:**
Erstelle eine `.env` Datei im Projekt-Root mit deinem OpenAI API Key:
```
OPENAI_API_KEY=sk-...
```

4. **Backend starten (Terminal 1):**
```bash
uv run python main.py
```
Der API Server startet auf `http://localhost:7777`

5. **Frontend starten (Terminal 2):**
```bash
cd frontend
uv run streamlit run app.py
```
Die Webanwendung öffnet sich auf `http://localhost:8501`

## 📁 Projektstruktur

```
.
├── main.py                 # FastAPI Backend mit Agno Agents
├── frontend/
│   └── app.py             # Streamlit Frontend
├── tmp/                    # SQLite Datenbank für Agent-Historie
├── .env                    # Umgebungsvariablen (API Keys)
├── pyproject.toml          # Projekt-Metadaten & Dependencies
└── README.md              # Diese Datei
```

## 🛠️ Technologie-Stack

- **Framework**: [Agno](https://github.com/phidatahq/agno) - Agentic Framework
- **Backend**: FastAPI
- **Frontend**: Streamlit
- **KI-Modell**: OpenAI GPT-4o-mini
- **Datenbank**: SQLite
- **APIs**: DuckDuckGo, arXiv, Yahoo Finance, HackerNews

## 📝 Verwendung

1. Öffne die Streamlit-Anwendung im Browser
2. Wähle zwischen Text- oder Voice-Input
3. Stelle eine Frage an das Research Team
4. Das System verteilt die Anfrage an spezialisierte Agenten
5. Erhalte eine koordinierte Antwort mit Audio-Ausgabe

### Beispielabfragen:
- "Was sind die neuesten Tech-Trends?"
- "Finde aktuelle Forschungspaper über Machine Learning"
- "Wie sieht die Tesla-Aktie aus?"
- "Suche nach den besten Python-Frameworks"

## 📚 Weitere Ressourcen

- [Agno Dokumentation](https://github.com/phidatahq/agno)
- [OpenAI API Referenz](https://platform.openai.com/docs)
- [FastAPI Dokumentation](https://fastapi.tiangolo.com/)
- [Streamlit Dokumentation](https://docs.streamlit.io/)

## 👨‍💼 Autor

**Marios Tzialidis**  
[DFT IT](https://dft-it.de/)

## 🤝 Contributing

Dieses Projekt ist öffentlich und Contributions sind gerne gesehen! Wenn du:
- Bugs gefunden hast
- Verbesserungsvorschläge hast
- Neue Features hinzufügen möchtest
- Dokumentation verbessern willst

Dann erstelle gerne einen **Pull Request** oder öffne ein **Issue** im [Repository](https://github.com/DFT-IT/agno-ai-agent-project).

### Wie du beitragen kannst:
1. Fork das Repository
2. Erstelle einen Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit deine Änderungen (`git commit -m 'Add some AmazingFeature'`)
4. Push zum Branch (`git push origin feature/AmazingFeature`)
5. Öffne einen Pull Request

## 📄 Lizenz

Dieses Projekt ist ein Lernprojekt. Nutzung auf eigenes Risiko.

---

**Repository**: https://github.com/DFT-IT/agno-ai-agent-project.git
