import json
import os
from groq import Groq
import ollama

class Summarizer:
    def __init__(self):
        # Load config from root directory
        config_path = os.path.join(os.path.dirname(__file__), "..", "config.json")
        with open(config_path, "r") as f:
            self.config = json.load(f)["summarizer"]
        
        self.provider = self.config["provider"].lower()
        if self.provider == "groq":
            self.client = Groq(api_key=self.config["groq"]["api_key"])
            self.model = self.config["groq"]["model"]
        elif self.provider == "ollama":
            self.model = self.config["ollama"]["model"]
        else:
            raise ValueError(f"Unknown summarizer provider: {self.provider}")

    def summarize(self, data, results, ticker):
        prompt = f"""Provide a concise financial summary for {data['company']} ({ticker}) in bullet points.  
        Include key company details, followed by insights from the financial data, highlighting strengths, risks, and growth potential.  

        Company Overview: {data.get('company_overview', 'N/A')}  
        Industry: {data.get('industry', 'N/A')}  
        Market Cap: {data.get('market_cap', 'N/A')}  
        Stock Exchange: {data.get('exchange', 'N/A')}  
        (if the values are N/A, don't show that)

        Calculated Benefits: {results}  
        also summarize the Calculated Benefits data.

        Raw Data: {data}  
        
        """
        try:
            if self.provider == "groq":
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=500,
                    temperature=0.2
                )
                return response.choices[0].message.content
            elif self.provider == "ollama":
                response = ollama.chat(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}]
                )
                return response["message"]["content"]
        except Exception as e:
            return f"- Summary unavailable due to error: {str(e)}"