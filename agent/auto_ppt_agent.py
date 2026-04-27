import asyncio
import json
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
from config import Config


def get_llm():
    return ChatGroq(
        model=Config.MODEL_ID,
        api_key=Config.GROQ_API_KEY,
        temperature=0.5,  # increased for richer content
    )


async def generate_content(llm, topic: str) -> dict:
    """Ask LLM to generate all slide content as JSON."""
    messages = [
        SystemMessage(content=(
            "You are a presentation content generator. "
            "Each bullet point must be detailed and contain 10-15 words. "
            "Do not generate short phrases. Avoid one-word or two-word points. "
            "Return ONLY valid JSON. No explanation. No markdown. No code blocks. "
            "Just raw JSON."
        )),
        HumanMessage(content=(
            f"Generate content for a 5-slide presentation about: {topic}\n\n"
            "Return this exact JSON structure:\n"
            "{\n"
            '  "title": "Main presentation title",\n'
            '  "subtitle": "One line subtitle",\n'
            '  "slides": [\n'
            '    {\n'
            '      "title": "Slide 2 title",\n'
            '      "bullet_points": [\n'
            '        "Detailed explanation of the concept with context and meaning (10-15 words)",\n'
            '        "Another meaningful point explaining importance or working clearly (10-15 words)",\n'
            '        "Explanation including example or real-world application (10-15 words)",\n'
            '        "Insight about benefits, impact, or significance (10-15 words)",\n'
            '        "Additional supporting detail to make slide content richer (10-15 words)"\n'
            '      ],\n'
            '      "image_query": "specific search term for image"\n'
            '    },\n'
            '    {\n'
            '      "title": "Slide 3 title",\n'
            '      "bullet_points": [\n'
            '        "Detailed explanation of the concept with context and meaning (10-15 words)",\n'
            '        "Another meaningful point explaining importance or working clearly (10-15 words)",\n'
            '        "Explanation including example or real-world application (10-15 words)",\n'
            '        "Insight about benefits, impact, or significance (10-15 words)",\n'
            '        "Additional supporting detail to make slide content richer (10-15 words)"\n'
            '      ],\n'
            '      "image_query": "specific search term for image"\n'
            '    },\n'
            '    {\n'
            '      "title": "Slide 4 title",\n'
            '      "bullet_points": [\n'
            '        "Detailed explanation of the concept with context and meaning (10-15 words)",\n'
            '        "Another meaningful point explaining importance or working clearly (10-15 words)",\n'
            '        "Explanation including example or real-world application (10-15 words)",\n'
            '        "Insight about benefits, impact, or significance (10-15 words)",\n'
            '        "Additional supporting detail to make slide content richer (10-15 words)"\n'
            '      ],\n'
            '      "image_query": "specific search term for image"\n'
            '    }\n'
            '  ],\n'
            '  "summary": "One sentence conclusion summary",\n'
            '  "takeaways": ["takeaway 1", "takeaway 2", "takeaway 3"]\n'
            "}"
        ))
    ]

    response = await llm.ainvoke(messages)
    raw = response.content.strip()

    # Clean markdown if present
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]

    raw = raw.strip()
    return json.loads(raw)


async def run_agent(user_prompt: str):

    if len(user_prompt.strip()) < 5:
        user_prompt = "Create a general informative presentation"
        print(f"⚠️ Vague prompt detected. Using default: '{user_prompt}'")

    print(f"\n Starting AutoPPT Agent for topic: '{user_prompt}'\n")

    client = MultiServerMCPClient({
        "ppt_server": {
            "command": "python",
            "args": ["mcp_servers/ppt_server.py"],
            "transport": "stdio"
        },
        "search_server": {
            "command": "python",
            "args": ["mcp_servers/search_server.py"],
            "transport": "stdio"
        }
    })

    tools = await client.get_tools()
    print(f" Loaded {len(tools)} tools: {[t.name for t in tools]}\n")

    tool_map = {t.name: t for t in tools}
    llm = get_llm()

    # Step 1 — Generate content
    print(" Generating slide content...\n")
    try:
        content = await generate_content(llm, user_prompt)
        print(f" Content generated:\n{json.dumps(content, indent=2)}\n")
    except Exception as e:
        print(f"Content generation failed: {e}")
        raise

    filename = Config.OUTPUT_FILE

    # Step 2 — plan_slides
    print(" Step 1: plan_slides")
    result = await tool_map["plan_slides"].ainvoke({
        "topic": user_prompt,
        "num_slides": 5
    })
    print(f" {result}\n")

    # Step 3 — search_web
    print("🔧 Step 2: search_web")
    result = await tool_map["search_web"].ainvoke({
        "query": user_prompt
    })
    print(f" {result[:100]}...\n")

    # Step 4 — create_presentation
    print(" Step 3: create_presentation")
    result = await tool_map["create_presentation"].ainvoke({
        "filename": filename
    })
    print(f"{result}\n")

    # Step 5 — add_intro_slide
    print(" Step 4: add_intro_slide")
    result = await tool_map["add_intro_slide"].ainvoke({
        "filename": filename,
        "title": content["title"],
        "subtitle": content["subtitle"]
    })
    print(f" {result}\n")

    # Step 6 — add_content_slide
    for i, slide in enumerate(content["slides"], start=2):
        print(f" Step {i + 3}: add_content_slide (Slide {i})")
        result = await tool_map["add_content_slide"].ainvoke({
            "filename": filename,
            "title": slide["title"],
            "bullet_points": slide["bullet_points"],
            "image_query": slide["image_query"]
        })
        print(f" {result}\n")

    # Step 7 — add_conclusion_slide
    print(" Step 8: add_conclusion_slide")
    result = await tool_map["add_conclusion_slide"].ainvoke({
        "filename": filename,
        "summary": content["summary"],
        "takeaways": content["takeaways"]
    })
    print(f" {result}\n")

    # Step 8 — save_presentation
    print(" Step 9: save_presentation")
    result = await tool_map["save_presentation"].ainvoke({
        "filename": filename
    })
    print(f" {result}\n")

    print(" All slides generated and saved!")
    print(f"\n Done! Open '{Config.OUTPUT_FILE}' to view your presentation.\n")