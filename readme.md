# 📊 Inventory-Based Company Analysis Agent

Author: Ajun Ravi
Email: ajunravi123@gmail.com

## 🎯 Overview

An intelligent web application designed to analyze financial data for inventory-based companies (manufacturing, retail) using `yfinance`. The agent calculates key benefits like Margin Rate Lift and Efficiency Re-Investment, presenting results through a modern UI with interactive tables and comprehensive summaries.

## ✨ Key Features

### 🏭 Core Analysis
- **Inventory-Focused:** Specialized analysis for companies with significant inventory holdings
- **Smart Ticker Mapping:** Converts company names to tickers using multiple providers:
  - Groq
  - Ollama
  - OpenFIGI
- **Financial Insights:** Comprehensive data collection via `yfinance`:
  - Revenue metrics
  - Market capitalization
  - Inventory costs
  - Custom benefit calculations

### 💫 User Interface
- Modern, responsive design powered by Tailwind CSS
- Interactive results table with dollar-formatted totals
- Elegant error handling with informative popups
- Clear data visualization and summaries

### 🔧 Technical Features
- Modular service architecture
- Configurable provider system
- Agentic workflow orchestration

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Node.js (optional, for frontend development)
- API Keys (optional):
  - Groq
  - OpenFIGI

### Installation

1. **Clone the Repository**
```bash
git clone <repository-url>
cd inventory-based-company-analysis
```

2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure Settings**

Create `config.json` in the project root:
```json
{
    "summarizer": {
        "provider": "groq",
        "groq": {
            "api_key": "<GROQ_KEY>",
            "model": "mixtral-8x7b-32768"
        },
        "ollama": {
            "model": "deepseek-r1:1.5b"
        }
    },
    "ticker_mapper": {
        "provider": "alphavantage",
        "alphavantage": {
            "api_key": "<alphavantage_key>"
        },
        "finnhub": {
            "api_key": "<finnhub_key>"
        },
        "groq": {
            "api_key": "<GROQ_KEY>",
            "model": "mixtral-8x7b-32768"
        },
        "ollama": {
            "model": "deepseek-r1:1.5b"
        }
    }
}
```

4. **Launch the Application**
```bash
uvicorn main:app --reload
```

Visit `http://localhost:8000` in your browser.

## 📖 Usage Guide

1. **Access the Application**
   - Open your browser
   - Navigate to `http://localhost:8000`

2. **Analyze a Company**
   - Enter company name (e.g., "Tesla") or ticker (e.g., "TSLA")
   - Click "Analyze"
   - View comprehensive results table and summary

3. **Interpret Results**
   - For inventory-based companies: View benefits table and total USD value
   - For non-inventory companies: Review explanation popup

## 🏗 Project Structure

```
project/
├── services/
│   ├── data_fetcher.py     # Financial data retrieval
│   ├── calculator.py       # Benefit metrics computation
│   ├── summarizer.py       # Results summarization
│   ├── ticker_mapper.py    # Company name resolution
│   └── workflow.py         # Workflow orchestration
├── static/
│   ├── index.html         # Frontend interface
│   ├── styles.css         # Styling
│   └── script.js          # Frontend logic
├── main.py               # FastAPI application
├── config.json          # Configuration
├── requirements.txt     # Dependencies
└── README.md           # Documentation
```

## 📝 Notes

- **Inventory Threshold:** Companies with negligible inventory (< $0) are excluded
- **Currency:** All financial data displayed in USD
- **Ticker Resolution:** Multiple provider options available for robust company identification

## 🔜 Future Development

- [ ] Implement data caching system
- [ ] Add support for alternative data sources
- [ ] Enhance visualization with interactive charts
- [ ] Expand analysis metrics

## 🤝 Contributing

We welcome contributions! Feel free to:
- Submit issues
- Propose new features
- Create pull requests

---

Made with ❤️ by [Ajun Ravi](mailto:ajunravi123@gmail.com)
