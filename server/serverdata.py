import os
from fastapi import  HTTPException
from pydantic import BaseModel
from mcp.server.fastmcp import FastMCP
import yfinance as yf
from openai import OpenAI
from dotenv import load_dotenv

from pydantic import BaseModel

class TradeInput(BaseModel):
    symbol: str        # e.g., "AAPL.NS" or "RELIANCE.NS"
    average_price: float
    quantity: int 

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL_NAME = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

# Initialize FastMCP server instance
mcp = FastMCP("Server", dependencies=["fastapi", "yfinance","mcp[cli]","mcp","openai"])

# Shared schema for input


@mcp.tool()
async def fetch_fundamentals(data: TradeInput):
    """
    MCP Data tool: Fetches company fundamentals using yfinance,
    supporting global tickers including Indian exchanges (e.g., NSE/BSE)."""
    print("fetching fundamentals")
    try:
        ticker = yf.Ticker(data.symbol)
        info = ticker.info
        
        # Check if we have valid data
        if not info or 'longName' not in info:
            raise HTTPException(status_code=404, detail="Ticker not found or no fundamentals available")
        
        # Get additional financial data
        cashflow = ticker.cashflow
        balance_sheet = ticker.balance_sheet
        news = ticker.news
        
        # Build fundamentals dictionary with all available information
        fundamentals = {
            'symbol': data.symbol,
            'name': info.get('shortName'),
            'price': info.get('regularMarketPrice'),
            'longName': info.get('longName'),
            'sector': info.get('sector'),
            'marketCap': info.get('marketCap'),
            'trailingPE': info.get('trailingPE'),
            'forwardPE': info.get('forwardPE'),
            'priceToBook': info.get('priceToBook'),
            'debtToEquity': info.get('debtToEquity'),
            'dividendYield': info.get('dividendYield'),
            'beta': info.get('beta')
        }
        
        # Calculate position metrics
        current_value = data.quantity * fundamentals['price'] if fundamentals['price'] else 0
        unrealized_pnl = (fundamentals['price'] - data.average_price) * data.quantity if fundamentals['price'] else 0
        percent_change = ((fundamentals['price'] / data.average_price) - 1) * 100 if data.average_price and fundamentals['price'] else 0
        
        # Create the prompt
        prompt = f"""
        # Financial Analysis System
        
        ## Role
        You are functioning as a professional financial analyst with expertise in equity valuation and portfolio management.
        
        ## Task
        Analyze the provided securities data and generate an investment recommendation based on quantitative metrics and the user's current position.
        
        ## Input Data
        ### Company Fundamentals:
        ```json
        {fundamentals}
        ```
        
        ### User Position Details:
        - Entry Price: ${data.average_price}
        - Quantity: {data.quantity} shares
        - Current Market Value: ${current_value:.2f}
        - Unrealized P&L: ${unrealized_pnl:.2f} ({percent_change:.2f}%)
        
        ## Financial Statement Analysis:
        The analysis includes data from recent cashflow statements, balance sheets, and income statements.
        
        ## Recent News:
        {news[:3] if news else "No recent news available"}
        ## Recent Cashflow Statement:
        {cashflow}
        ## Recent Balance Sheet:
        {balance_sheet}
        
        ## Output Requirements
        Provide a structured recommendation in JSON format with the following elements:
        ```json
        {{
            "action": "BUY/HOLD/SELL",
            "confidence_level": "HIGH/MEDIUM/LOW",
            "rationale": "Concise explanation supporting the recommendation",
            "key_metrics": ["List the 2-3 most influential metrics that informed your decision"],
            "risk_factors": ["Identify potential risks to this recommendation"]
        }}

        Ask for the ticker symbol if not provided by the user
        Ask for the average price if not provided by the user
        Ask for the quantity if not provided by the user
        ```
        """
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Error fetching fundamentals: {e}")
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "system", "content": "You are a helpful financial assistant."},
                      {"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=200
        )
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"LLM request failed: {e}")

    choice = response.choices[0].message.content.strip()
    return {"symbol": data.symbol, "fundamentals": fundamentals}

@mcp.tool()
async def fetch_news(data: TradeInput):
    """
    MCP Data tool: Fetches company news using yfinance,
    supporting global tickers including Indian exchanges (e.g., NSE/BSE)."""
    print("fetching news")
    try:
        ticker = yf.Ticker(data.symbol)
        news = ticker.news
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Error fetching news: {e}")

    return {"symbol": data.symbol, "news": news}


if __name__ == "__main__":
    # Launch MCP server
    mcp.run()

