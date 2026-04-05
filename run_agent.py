import asyncio
from agent.auto_ppt_agent import run_agent

if __name__ == "__main__":
    user_input = input("Enter topic: ")
    asyncio.run(run_agent(user_input))