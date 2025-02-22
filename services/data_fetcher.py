import yfinance as yf
from datetime import datetime
import pandas as pd

class DataFetcher:
    def __init__(self, ticker):
        self.ticker = ticker.upper()
        self.stock = yf.Ticker(ticker)

    def get_financials(self):
        try:
            info = self.stock.info
            if not info or info.get('symbol') is None:
                raise ValueError("Company not found. Please check the ticker and try again.")

            balance_sheet = self.stock.balance_sheet
            income_statement = self.stock.financials

            if balance_sheet.empty and income_statement.empty:
                raise ValueError("Company not found. Please check the ticker and try again.")

            latest_inventory_date = balance_sheet.columns[0] if not balance_sheet.empty else "Not Available"
            latest_financial_date = income_statement.columns[0] if not income_statement.empty else "Not Available"

            # Fetch inventory cost and handle NaN
            inventory_cost = balance_sheet.loc['Inventory', latest_inventory_date] if 'Inventory' in balance_sheet.index else "Not Available"
            if isinstance(inventory_cost, float) and pd.isna(inventory_cost):
                inventory_cost = "Not Available"

            # Check if the company has significant inventory
            if inventory_cost == "Not Available" or (isinstance(inventory_cost, (int, float)) and inventory_cost <= 0):
                raise ValueError(f"This application is designed for inventory-based companies only. '{self.ticker}' does not have significant inventory data.")

            cogs = income_statement.loc['Cost Of Revenue', latest_financial_date] if 'Cost Of Revenue' in income_statement.index else "Not Available"
            revenue = income_statement.loc['Total Revenue', latest_financial_date] if 'Total Revenue' in income_statement.index else 0
            gross_profit = income_statement.loc['Gross Profit', latest_financial_date] if 'Gross Profit' in income_statement.index else "Not Available"
            market_cap = self.stock.info.get('marketCap', 0)
            headcount = self.stock.info.get('fullTimeEmployees', "Not Available")
            sga_expense = income_statement.loc['Selling General And Administration', latest_financial_date] if 'Selling General And Administration' in income_statement.index else "Not Available"
            cost_of_revenue = income_statement.loc['Cost Of Revenue', latest_financial_date] if 'Cost Of Revenue' in income_statement.index else 0

            gross_profit_percentage = (gross_profit / revenue * 100) if isinstance(gross_profit, (int, float)) and revenue > 0 else "Not Available"
            eff_high = revenue / headcount if headcount != "Not Available" and revenue > 0 else "Not Available"
            eff_low = cost_of_revenue / headcount if headcount != "Not Available" and cost_of_revenue > 0 else "Not Available"
            salary_avg = sga_expense / headcount if headcount != "Not Available" and sga_expense != "Not Available" else "Not Available"

            return {
                "company": self.ticker,
                "analized_data_date": latest_inventory_date,
                "balance_sheet_inventory_cost": inventory_cost,
                "P&L_inventory_cost": cogs,
                "Revenue": revenue,
                "Headcount Old": headcount,
                "Efficiency Output High": eff_high,
                "Efficiency Output Low": eff_low,
                "Salary Average": salary_avg,
                "gross_profit": gross_profit,
                "gross_profit_percentage": gross_profit_percentage,
                "market_cap": market_cap
            }
        except Exception as e:
            raise ValueError("Company not found. Please try with correct ticker string.")
            # raise ValueError(str(e))  # Blocking the system errors to user

    def get_company_type(self, market_cap, revenue):
        if revenue > 50e9 and market_cap > 200e9:
            return "Global"
        elif revenue > 10e9 and market_cap > 50e9:
            return "Leader"
        elif revenue > 1e9 and market_cap > 10e9:
            return "Challenger"
        else:
            return "Startup"