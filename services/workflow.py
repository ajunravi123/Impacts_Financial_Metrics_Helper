from services.data_fetcher import DataFetcher
from services.calculator import Calculator
from services.summarizer import Summarizer
from services.ticker_mapper import TickerMapper

class Workflow:
    def __init__(self):
        self.fetcher = DataFetcher
        self.calculator = Calculator()
        self.summarizer = Summarizer()
        self.mapper = TickerMapper()

    def analyze(self, input_str):
        ticker = self.mapper.get_ticker(input_str)
        
        fetcher = self.fetcher(ticker)
        try:
            raw_data = fetcher.get_financials()
            raw_data["company_type"] = fetcher.get_company_type(raw_data["market_cap"], raw_data["Revenue"])
        except ValueError as e:
            
            return {"error": str(e)}

        benefits = self.calculator.calculate_benefits(raw_data)
        summary = self.summarizer.summarize(raw_data, benefits, ticker)

        return {"raw_data": raw_data, "benefits": benefits, "summary": summary}