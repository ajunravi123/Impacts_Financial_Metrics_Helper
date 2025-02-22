class Calculator:
    def __init__(self):
        self.benefit_mapping = {
            "Global": {
                "Margin Rate Lift (bps)": (1.00, 1.50),
                "Margin on Revenue Lift": (0.50, 1.00),
                "Efficiency Re-Investment": (100, 200),
                "Reduction in Xfer Expenses": (0.020, 0.024),
                "Inventory Carrying Costs": (5.0, 12.0)
            },
            "Leader": {
                "Margin Rate Lift (bps)": (0.75, 1.20),
                "Margin on Revenue Lift": (0.40, 0.80),
                "Efficiency Re-Investment": (75, 150),
                "Reduction in Xfer Expenses": (0.015, 0.020),
                "Inventory Carrying Costs": (3.0, 10.0)
            },
            "Challenger": {
                "Margin Rate Lift (bps)": (0.50, 1.00),
                "Margin on Revenue Lift": (0.30, 0.60),
                "Efficiency Re-Investment": (50, 100),
                "Reduction in Xfer Expenses": (0.010, 0.016),
                "Inventory Carrying Costs": (2.0, 8.0)
            },
            "Startup": {
                "Margin Rate Lift (bps)": (0.25, 0.80),
                "Margin on Revenue Lift": (0.10, 0.50),
                "Efficiency Re-Investment": (30, 80),
                "Reduction in Xfer Expenses": (0.005, 0.012),
                "Inventory Carrying Costs": (1.0, 5.0)
            }
        }

    def calculate_benefits(self, values):
        company_type = values["company_type"]
        percentages = self.benefit_mapping.get(company_type, self.benefit_mapping["Startup"])
        revenue = values["Revenue"] if values["Revenue"] != "Not Available" else 0
        inventory_cost = values["balance_sheet_inventory_cost"] if values["balance_sheet_inventory_cost"] != "Not Available" else 0
        gross_profit = values["gross_profit"] if values["gross_profit"] != "Not Available" else 0
        gross_profit_pct = values["gross_profit_percentage"] if values["gross_profit_percentage"] != "Not Available" else 0
        headcount = values["Headcount Old"] if values["Headcount Old"] != "Not Available" else 0
        salary_avg = values["Salary Average"] if values["Salary Average"] != "Not Available" else 0

        def safe_calc(low, high, calc_func):
            try:
                return {"low": calc_func(low), "high": calc_func(high)}
            except:
                return {"low": "Not Available", "high": "Not Available"}

        results = {
            "Margin_Rate_Lift": safe_calc(
                percentages["Margin Rate Lift (bps)"][0], percentages["Margin Rate Lift (bps)"][1],
                lambda x: (revenue * ((gross_profit_pct / 100) + (x / 100))) - gross_profit if revenue and gross_profit else "Not Available"
            ),
            "Margin_on_Revenue_Lift": safe_calc(
                percentages["Margin on Revenue Lift"][0], percentages["Margin on Revenue Lift"][1],
                lambda x: ((revenue * (1 + (x / 100))) * (gross_profit_pct / 100)) - gross_profit if revenue and gross_profit else "Not Available"
            ),
            "Efficiency_Re_Investment": safe_calc(
                percentages["Efficiency Re-Investment"][0], percentages["Efficiency Re-Investment"][1],
                lambda x: (headcount - (headcount * 100 / (x + 100))) * salary_avg if headcount and salary_avg else "Not Available"
            ),
            "Reduction_in_Xfer_Expenses": safe_calc(
                percentages["Reduction in Xfer Expenses"][0], percentages["Reduction in Xfer Expenses"][1],
                lambda x: (x / 100) * inventory_cost if inventory_cost else "Not Available"
            ),
            "Inventory_Carrying_Costs": safe_calc(
                percentages["Inventory Carrying Costs"][0], percentages["Inventory Carrying Costs"][1],
                lambda x: (inventory_cost * 0.2) * (x / 100) if inventory_cost else "Not Available"
            )
        }
        return results