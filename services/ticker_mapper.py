import json
import os
from groq import Groq
import ollama
import re
import finnhub
import requests



class TickerMapper:
    def __init__(self):
        # Load config from root directory
        config_path = os.path.join(os.path.dirname(__file__), "..", "config.json")
        with open(config_path, "r") as f:
            config = json.load(f)
        
        self.provider = config["ticker_mapper"]["provider"].lower()
        if self.provider in ["finnhub", "alphavantage"]:
            self.finnhub_api_key = config["ticker_mapper"]["finnhub"]["api_key"]
            self.alphavantage_api_key = config["ticker_mapper"]["alphavantage"]["api_key"]
        elif self.provider == "groq":
            self.client = Groq(api_key=config["ticker_mapper"]["groq"]["api_key"])
            self.model = config["ticker_mapper"]["groq"]["model"]
        elif self.provider == "ollama":
            self.model = config["ticker_mapper"]["ollama"]["model"]
        else:
            raise ValueError(f"Unsupported ticker_mapper provider: {self.provider}")

    def get_ticker(self, input_str, provider = ''):
        input_str = input_str.lower().strip()
        
        # If it looks like a ticker (all caps, short), assume it’s a ticker
        if input_str.isupper() and 1 <= len(input_str) <= 5:
            return input_str

        # Use the selected provider to find the ticker
        prompt = f"What is the primary stock ticker symbol for the company '{input_str}'? Return only the ticker symbol (e.g., 'TSLA') with no additional text, or 'Not Found' if unknown."
        try:
            if provider != '':
                self.provider = provider

            if self.provider == "alphavantage":
                url = f"https://www.alphavantage.co/query"

                params = {
                    "function": "SYMBOL_SEARCH",
                    "keywords": input_str,
                    "apikey": self.alphavantage_api_key
                }
                
                response = requests.get(url, params=params)
                data = response.json()
                if "bestMatches" in data and data["bestMatches"]:
                    return data["bestMatches"][0]["1. symbol"]
                else:
                    return self.get_ticker(input_str, 'finnhub')
            elif self.provider == "finnhub":
                finnhub_client = finnhub.Client(api_key=self.finnhub_api_key)
                results = finnhub_client.symbol_lookup(input_str)
                ticker = results["result"][0]["symbol"] if results["count"] > 0 else None
                return input_str if ticker == None or ticker == "" else ticker
            elif self.provider == "groq":
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=10,
                    temperature=0.1
                )
                ticker = response.choices[0].message.content.strip()
                # Post-process to extract the first valid ticker if needed
                match = re.search(r'\b[A-Z]{2,5}\b', ticker)
                if match:
                    return match.group(0)  # e.g., "GOOGL" from "GOOGL or GOOG"
            elif self.provider == "ollama":
                response = ollama.chat(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}]
                )
                ticker = response["message"]["content"].strip()
                # Post-process to extract the first valid ticker if needed
                match = re.search(r'\b[A-Z]{2,5}\b', ticker)
                if match:
                    return match.group(0)  # e.g., "GOOGL" from "GOOGL or GOOG"

            
            return ticker if ticker == "Not Found" else input_str  # Fallback if no ticker found
        except Exception as e:
            print(f"Error fetching ticker with {self.provider} for '{input_str}': {e}")
            return input_str  # Let DataFetcher handle invalid ticker errors