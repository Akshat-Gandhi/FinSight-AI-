from textwrap import dedent
import asyncio
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from mcp_use import MCPAgent, MCPClient
from halo import Halo

async def run_memory_chat():
    """Run a chat using MCPAgent's built-in conversation memory."""
    # Load environment variables for API keys
    load_dotenv()

    # Config file path - change this to your config file
    config_file = "server/mcp_server.json"

    print("Initializing chat...")

    # Create MCP client and agent with memory enabled
    client = MCPClient.from_config_file(config_file)
    llm = ChatOpenAI(model="gpt-4o-mini",api_key=os.getenv("OPENAI_API_KEY"))

    # Create agent with memory_enabled=True
    agent = MCPAgent(
        llm=llm,
        client=client,
        max_steps=15,
        memory_enabled=True, 
        system_prompt="You are a helpful financial assistant. You are given a list of companies and you need to analyze the fundamentals of the company and provide a recommendation on whether to buy, sell or hold the stock. You are also given the historical data of the stock and you need to analyze the data and provide a recommendation on whether to buy, sell or hold the stock. when you are given a compnay name then you need to first find the ticker symbol of the company and then you need to analyze the fundamentals of the company and provide a recommendation on whether to buy, sell or hold the stock." # Enable built-in conversation memory
    )


    print(dedent("""
        🎯 Hello! Fellow Analyst can assist you in various financial and investment-related tasks, including:

        1️⃣  Company Analysis:    Insights on fundamentals and performance.
        2️⃣  Ticker Lookup:       Find the company's stock symbol.
        3️⃣  Recommendations:     Buy, sell, or hold guidance.
        4️⃣  News Updates:        Latest relevant company news.

        🛡️  Disclaimer

        ⚠️  Important Notice:
            This tool is currently in **BETA** and is intended for **informational and educational purposes only**.
            Recommendations are **not guaranteed** to be accurate or complete.
            Users must conduct their **own independent research and analysis** before making any investment decisions.

        📉  Investment Risks:
            Investments are subject to market risks, including the potential loss of principal.
            Past performance is not indicative of future results.
            Please consult with a qualified financial advisor to assess the suitability of any investment
            for your personal circumstances.

        ⚠️  Warning: You must provide exactly three values—**ticker symbol**, **average buying price**, and **total quantity**.
    """))


    try:
        # Main chat loop
        while True:
            # Get user input
            print("\nUSER: ")
            user_input = input()
            # Check for exit command
            if user_input.lower() in ["exit", "quit"]:
                print("Ending conversation...")
                break

            # Check for clear history command
            if user_input.lower() == "clear":
                agent.clear_conversation_history()
                print("Conversation history cleared.")
                continue

            # Get response from agent
            print("\nAssistant: ", end="", flush=True)
            spinner = Halo(text="Analyzing...", spinner="dots")
            spinner.start()
            try:
                response = await agent.run(user_input)
                spinner.succeed("ASSISTANT: ")
            except Exception as e:
                spinner.fail("Error")
                raise
            print(response)


    finally:
        # Clean up
        if client and client.sessions:
            await client.close_all_sessions()


if __name__ == "__main__":
    asyncio.run(run_memory_chat())


