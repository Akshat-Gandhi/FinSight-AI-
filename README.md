
A sophisticated Python-based trading and market analysis platform powered by AI.

## 📋 Overview

mcp-trading-ai is a modern Python application that combines  LangChain, OpenAI, and yfinance to create a powerful platform for financial market analysis and trading. The system features a robust client-server architecture with advanced AI capabilities, designed to process complex financial data and generate intelligent trading insights.

Key capabilities include:
- Real-time market data processing and analysis
- AI-powered financial insights and predictions
- Automated trading signal generation
- Portfolio analysis and risk assessment
- Market sentiment analysis using advanced NLP
- Historical data analysis and pattern recognition

The system is built with scalability and performance in mind, making it suitable for both individual traders and institutional users. Its modular architecture allows for easy extension and customization of features.

## ✨ Features

- 🚀 FastAPI-based server implementation with high performance and async support
- 🤖 LangChain and OpenAI integration for advanced AI-powered features
- 📊 yfinance integration for real-time financial data and market analysis
- 🔌 Client-server architecture for distributed processing
- 🛠️ Modern Python tooling with pyproject.toml and uv.lock
- 🔒 Secure environment variable management with python-dotenv
- 📦 Type-safe data handling with Pydantic models

## 📋 Prerequisites

- Python 3.13 or higher
- pip or uv package manager
- Git for version control

## 📁 Project Structure

```
mcp-trading-ai/
├── main.py              # 🚀 Main application entry point
├── client.py            # 💻 Client implementation
├── core_class.py        # 🏗️ Core class definitions
├── server/              # 🌐 Server implementation
├── Test.mp4            # 🎥 Demo video
├── pyproject.toml       # ⚙️ Project configuration
├── uv.lock             # 🔒 Dependency lock file
└── .env                 # 🔒 Environment variables
```

## 🎥 Demo Video

A demonstration video (`Test.mp4`) is included in the project root directory. This video showcases the key features and functionality of the platform, including:
- System setup and configuration
- Real-time market data processing
- AI-powered analysis features
- Trading signal generation
- User interface walkthrough

## 📦 Dependencies

- LangChain >= 0.1.0 - Framework for developing AI applications
- OpenAI >= 1.0.0 - OpenAI API integration
- yfinance >= 0.2.0 - Yahoo Finance market data
- Python-dotenv >= 1.0.0 - Environment variable management
- Pydantic >= 2.0.0 - Data validation and settings management

