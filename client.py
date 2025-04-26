import asyncio
import os
import sys
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from mcp_use import MCPAgent, MCPClient

def loading_animation():
    """Display a simple loading animation."""
    chars = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
    for char in chars:
        sys.stdout.write(f"\r{char} Analyzing data... ")
        sys.stdout.flush()

async def run_memory_chat():
    """Run a chat using MCPAgent's built-in conversation memory."""
    # Load environment variables for API keys
    load_dotenv()

    # Config file path - change this to your config file
    config_file = "server/mcp_server.json"

    print("Initializing chat...")

    # Create MCP client and agent with memory enabled
    client = MCPClient.from_config_file(config_file)
    
    # Initialize OpenAI model with system prompt
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        api_key=os.getenv("OPENAI_API_KEY")
    )

    # Create agent with memory_enabled=True
    agent = MCPAgent(
        llm=llm,
        client=client,
        max_steps=15,
        memory_enabled=True,
        system_prompt="""You are a helpful financial assistant. You are given a list of companies and you need to analyze the fundamentals of the company and provide a recommendation on whether to buy, sell or hold the stock. You are also given the historical data of the stock and you need to analyze the data and provide a recommendation on whether to buy, sell or hold the stock. Always gather the news for the company while making recommendations."""
    )

    print("\n===== 🚀 Interactive MCP Chat 🚀 =====")
    print("Type 'exit' or 'quit' to end the conversation 🔚")
    print("Type 'clear' to clear conversation history 🧹")
    print("======================================\n")
    print('''🔍 Hello, Fellow Analyst! I'm here to assist you with various financial and investment-related tasks, including:

            1. 📊 **Company Analysis**: In-depth insights and analysis on specific companies, including their fundamentals and stock performance.

            2. 💡 **Investment Recommendations**: With historical data and fundamentals in hand, I can suggest whether it's time to buy, sell, or hold a stock.

            3. 📰 **News Updates**: Stay up-to-date with the latest news, offering valuable context and insights that could influence stock performance.

            Whether you have a specific company in mind or need help making investment decisions, just let me know! 💬
            Ready when you are!''')

    try:
        # Get initial input
        print("\nEnter the company ticker symbol: ")
        ticker_symbol = input().strip().upper()
        
        print("Enter the average buying price: ")
        try:
            average_price = float(input().strip())
        except ValueError:
            print("Invalid price. Please enter a valid number.")
            return
            
        print("Enter the total quantity: ")
        try:
            quantity = int(input().strip())
        except ValueError:
            print("Invalid quantity. Please enter a valid whole number.")
            return

        # Main chat loop
        while True:
            print("\nAdditional information (or type 'exit' to quit): ")
            additional_info = input().strip()
            
            if additional_info.lower() in ["exit", "quit"]:
                print("Ending conversation...")
                break
                
            if additional_info.lower() == "clear":
                agent.clear_conversation_history()
                print("Conversation history cleared.")
                continue

            # Format the input for the agent
            user_input = f"Ticker: {ticker_symbol}, Average Price: ${average_price:.2f}, Quantity: {quantity}, Additional Info: {additional_info}"

            # Get response from agent
            print("\nAssistant: ", end="", flush=True)

            try:
                # Start loading animation in a separate thread
                loading_task = asyncio.create_task(asyncio.to_thread(loading_animation))
                
                # Run the agent with the user input
                response = await agent.run(user_input)
                
                # Stop loading animation
                loading_task.cancel()
                print("\r" + " " * 50 + "\r", end="")  # Clear the loading line
                
                print(response)

            except Exception as e:
                print(f"\nError: {e}")

    finally:
        # Clean up
        if client and client.sessions:
            await client.close_all_sessions()

if __name__ == "__main__":
    asyncio.run(run_memory_chat())


