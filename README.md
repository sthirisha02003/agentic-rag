# Agentic RAG

Agentic RAG using CrewAI — searches documents and falls back to web search.

## Features
- Multi-document RAG with per-source attribution
- Smart web search fallback with credibility scoring
- Supports GPT-4o, DeepSeek-R1, and Llama 3.2

## Requirements
- Python 3.11+
- FireCrawl API key
- OpenAI API key
- Qdrant (local or cloud)

## Installation

1. Clone the repository
   git clone https://github.com/sthirisha02003/agentic-rag.git
   cd agentic-rag

2. Install dependencies
   pip install streamlit crewai crewai-tools qdrant-client fastembed python-dotenv

3. Set up environment variables
   Copy .env.example to .env and fill in your API keys
   FIRECRAWL_API_KEY=your_key_here
   OPENAI_API_KEY=your_key_here

4. Run the app
   streamlit run app.py

## Project Structure
- app.py        — Streamlit UI
- main.py       — CrewAI crew entry point
- src/          — Agents, tasks, and tools
