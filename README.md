# 🤖 Auto PPT Agent

An AI-powered agent that automatically generates PowerPoint presentations from a single user prompt — no manual slide creation needed.

Built using LangChain, Groq LLM, and MCP (Model Context Protocol).


## 📽️ Demo

Enter a prompt like:
"Create a 5-slide presentation about Machine Learning"

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
│
├── agent/
│   └── auto_ppt_agent.py      # Agent logic (LangChain + tools)
│
├── mcp_servers/
│   ├── ppt_server.py          # PPT generation tools
│   └── search_server.py       # Web search tool
│
├── app.py                     # Streamlit frontend
├── run_agent.py               # CLI entry point
├── config.py                  # API keys & settings
├── requirements.txt
└── reflection.md

## ⚙️ Setup and Installation

Clone the repository and move into the project folder.

Install all required dependencies using the requirements file.

Get your API keys:

Groq API key from https://console.groq.com
Pexels API key from https://www.pexels.com/api

Open the config.py file and replace the placeholder values with your API keys.

To run the application using the web interface, start the Streamlit app. This provides a simple UI where you can enter your prompt and generate presentations interactively.

Alternatively, you can run the agent directly from the terminal, which will prompt you to enter a topic and generate the presentation.

Once the process completes, the generated PowerPoint file will be saved in the project directory. Open the file to view your presentation.

## 🛠️ MCP Tools

ppt_server.py exposes four tools — plan_slides, create_presentation, add_slide, and save_presentation. Each tool is fully documented with docstrings so the agent knows exactly when and how to call them.

search_server.py exposes one tool — search_web — which fetches a summary from Wikipedia for the given topic. If the search fails, the agent gracefully falls back to its own knowledge instead of crashing.

## 🧪 Testing MCP Servers

Use the MCP Inspector to test each tool interactively in a browser UI.

npx @modelcontextprotocol/inspector python mcp_servers/ppt_server.py

npx @modelcontextprotocol/inspector python mcp_servers/search_server.py

Opens at http://localhost:5173 — click Connect, go to the Tools tab, and run each tool manually with your own inputs.


## 📦 Tech Stack
  -LLM — Groq (llama-3.3-70b-versatile)
  -Agent Framework — LangChain  
  -Protocol — MCP (Model Context Protocol)
  -Frontend — Streamlit
  -PPT Generation — python-pptx
  -Images — Pexels API
  -Search — Wikipedia REST API


## 💡 Example Prompts

    "Deep Learning vs Machine Learning",
    "Blockchain Technology and Its Applications",
    "Cloud Computing Architecture",
    "Cybersecurity Threats and Prevention",
    "Operating System Concepts",
    "Evolution of Artificial Intelligence"
