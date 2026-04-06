# 🤖 Auto PPT Agent

An AI-powered agent that automatically generates PowerPoint presentations from a single user prompt — no manual slide creation needed.

Built using LangChain, Groq LLM, and MCP (Model Context Protocol).


## 📽️ Demo

Enter a prompt like:
"Create a 5-slide presentation on the life cycle of a star for a 6th-grade class"

The agent plans, searches, writes, and saves a .pptx file — all by itself.


## 🏗️ Architecture

User Prompt → Agent Brain (Groq LLM) → MCP Tool Loop → output.pptx

The agent follows this sequence every time:
1. plan_slides — decides the structure before touching any file
2. search_web — fetches real information about the topic
3. create_presentation — initializes the .pptx file on disk
4. add_slide × 5 — writes each slide with title and bullet points
5. save_presentation — confirms the file is saved


## 📁 Project Structure

auto_ppt_agent/
- agent/auto_ppt_agent.py — main agent loop
- mcp_servers/ppt_server.py — MCP tools for PPT creation
- mcp_servers/search_server.py — MCP tool for web search
- config.py — model and file settings
- run_agent.py — entry point
- requirements.txt
- reflection.md


## ⚙️ Setup and Installation

Step 1 — Clone the repository

git clone https://github.com/VasaviKalyaniPinnam/AutoPPTAgent.git
cd AutoPPTAgent

Step 2 — Install dependencies

pip install -r requirements.txt

Step 3 — Add your Groq API key

Get a free key at https://console.groq.com, then open config.py and replace the placeholder with your key.

Step 4 — Run the agent

python run_agent.py

Step 5 — Enter your prompt

Enter topic: Create a 5-slide presentation on the solar system for 6th graders

Step 6 — Open the output

start output.pptx


## 🛠️ MCP Tools

ppt_server.py exposes four tools — plan_slides, create_presentation, add_slide, and save_presentation. Each tool is fully documented with docstrings so the agent knows exactly when and how to call them.

search_server.py exposes one tool — search_web — which fetches a summary from Wikipedia for the given topic. If the search fails, the agent gracefully falls back to its own knowledge instead of crashing.

## 🧪 Testing MCP Servers

Use the MCP Inspector to test each tool interactively in a browser UI.

npx @modelcontextprotocol/inspector python mcp_servers/ppt_server.py

npx @modelcontextprotocol/inspector python mcp_servers/search_server.py

Opens at http://localhost:5173 — click Connect, go to the Tools tab, and run each tool manually with your own inputs.


## 📦 Tech Stack

- LLM — Groq (llama-3.3-70b-versatile)
- Agent Framework — LangChain
- Tool Protocol — MCP (Model Context Protocol)
- PPT Generation — python-pptx
- Web Search — Wikipedia REST API


## 💡 Example Prompts

- Create a 5-slide presentation on black holes for high school students
- Create a presentation on the history of the internet
- Make a presentation about climate change for college students
- Create slides on photosynthesis for 8th graders
