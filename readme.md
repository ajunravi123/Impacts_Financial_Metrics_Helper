# Inventory-Based Company Analysis Agent

Author: Ajun Ravi
Email: ajunravi123@gmail.com


This is an agentic web application designed to analyze financial data for inventory-based companies (e.g., manufacturing, retail) using `yfinance`. It provides calculated benefits like Margin Rate Lift, Efficiency Re-Investment, and more, with a modern UI featuring a results table, summary, and total benefits displayed in USD.

## Features
- **Inventory Focus**: Analyzes only companies with significant inventory (excludes tech/services like Google).
- **Ticker Mapping**: Converts company names to tickers using configurable providers (Groq, Ollama, or OpenFIGI).
- **Financial Data**: Fetches data via `yfinance` (revenue, market cap, inventory cost, etc.).
- **Benefit Calculations**: Computes low/high estimates for key metrics (e.g., Margin Rate Lift, Inventory Carrying Costs).
- **UI**: 
  - Beautiful results table with dollar-formatted totals.
  - Elegant popup for errors (e.g., non-inventory companies).
  - Responsive design with Tailwind CSS.
- **Configurable**: Uses `config.json` to switch ticker mapping and summarization providers.
- **Agentic Workflow**: Modular services (`DataFetcher`, `Calculator`, `Summarizer`, `TickerMapper`) orchestrated via `Workflow`.

## Prerequisites
- **Python 3.8+**
- **Node.js** (optional, only for local frontend tweaks)
- **Dependencies**: Listed in `requirements.txt`
- **Groq API Key** (optional, for ticker mapping or summarization)
- **Ollama** (optional, run locally for ticker mapping or summarization)
- **OpenFIGI API Key** (optional, alternative ticker mapping)

## Setup
1. **Clone the Repository**:
   ```
   git clone <repository-url>
   cd inventory-based-company-analysis

2. Install Dependencies:

pip install -r requirements.txt
Includes fastapi, uvicorn, yfinance, groq, ollama, jinja2.

Configure config.json: Located at the project root.

Example:

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
        "alphavantage" : {
            "api_key": "<alphavantage_key>"
        },
        "finnhub" : {
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

3. Run the Application:

uvicorn main:app --reload
Access at http://localhost:8000.

Usage
Open the Web UI:
Navigate to http://localhost:8000 in your browser.

Enter a Company:
Input a company name (e.g., "Tesla") or ticker (e.g., "TSLA") in the text field.

Click "Analyze".


4. View Results:

Inventory-Based Companies: Displays a table with benefits (e.g., Margin Rate Lift), a total benefit row in USD ($), and a summary.
Non-Inventory Companies: Shows a popup: "This application is designed for inventory-based companies only. '<ticker>' does not have significant inventory data."
Close Popups: Click "Close" on error messages to dismiss them.
Project Structure

project/
├── services/
│   ├── data_fetcher.py       # Fetches financial data with yfinance
│   ├── calculator.py         # Calculates benefit metrics
│   ├── summarizer.py         # Summarizes results (Groq/Ollama)
│   ├── ticker_mapper.py      # Maps names to tickers (Groq/Ollama/OpenFIGI)
│   └── workflow.py           # Orchestrates agentic workflow
├── static/
│   ├── index.html            # Frontend UI
│   ├── styles.css            # Custom CSS
│   └── script.js             # Frontend logic
├── main.py                   # FastAPI app
├── config.json               # Configuration file
├── requirements.txt          # Python dependencies
└── README.md                 # This file



Example Inputs

"Tesla" or "TSLA": Shows financial data and totals (inventory-based).
"Walmart" or "WMT": Similar (retail, inventory-heavy).
"Google" or "GOOGL": Popup error (non-inventory-based).


Notes

Inventory Check: Companies with no or negligible inventory (< $0) are excluded.
Currency: Financial amounts are in USD, displayed with $ in the UI.
Ticker Mapping: Groq/Ollama may occasionally return sentences; consider OpenFIGI for robustness (see ticker_mapper.py alternative).



Future Enhancements

Add caching for ticker mappings and financial data.
Support multiple data sources (e.g., Alpha Vantage) via data_fetcher.
Enhance UI with charts for benefit metrics.
Contributing
Feel free to submit issues or PRs to improve functionality or fix bugs!