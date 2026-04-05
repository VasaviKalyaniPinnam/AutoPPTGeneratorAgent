# Auto PPT Agent

Course: AI Agents & MCP Architecture  

##Where did my agent fail its first attempt?

It failed multiple times before it worked.

First, I tried using free HuggingFace models like `DialoGPT` and
`zephyr-7b-beta`. They all threw the same error ,the models simply
weren't supported by HuggingFace's inference API. I wasted time trying
three different models before realizing the entire approach was wrong.
Switched to Groq's free API and it connected instantly.


# What I learnt now

I'd test the MCP server with the Inspector tool first before connecting
it to the agent. I spent a lot of time debugging issues that the
Inspector would have caught in 30 seconds.


 Building this taught me that agentic AI isn't about writing smarter code — it's about building systems that can recover from their own mistakes.