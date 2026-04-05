import pandas as pd

class DataAnalyzer:
    def __init__(self, filepath):
        self.filepath = filepath
        self.df = None

    def load_data(self):
        try:
            self.df = pd.read_excel(self.filepath)
            print(f"Successfully loaded data from {self.filepath}")
            print(f"Data shape: {self.df.shape}")
            return True
        except Exception as e:
            print(f"Error loading data: {e}")
            return False

    def get_summary_statistics(self):
        if self.df is None:
            return "No data loaded."
            
        summary = {
            "total_rows": len(self.df),
            "columns": list(self.df.columns),
            "date_range": {
                "start": str(self.df['Date'].min().date()),
                "end": str(self.df['Date'].min().date())
            },
            "total_sales_revenue": round(self.df['Sales Revenue'].sum(), 2),
            "total_profit": round(self.df['Profit'].sum(), 2),
            "total_units_sold": int(self.df['Units Sold'].sum())
        }
        
        return summary

    def get_performance_by_region(self):
        if self.df is None or 'Region' not in self.df.columns:
            return {}
            
        region_sales = self.df.groupby('Region')['Sales Revenue'].sum().round(2).to_dict()
        region_profit = self.df.groupby('Region')['Profit'].sum().round(2).to_dict()
        
        return {
            "sales_by_region": region_sales,
            "profit_by_region": region_profit
        }

    def get_performance_by_product(self):
        if self.df is None or 'Product' not in self.df.columns:
            return {}
            
        product_sales = self.df.groupby('Product')['Sales Revenue'].sum().round(2).to_dict()
        product_units = self.df.groupby('Product')['Units Sold'].sum().to_dict()
        
        return {
            "sales_by_product": product_sales,
            "units_by_product": product_units
        }

    def generate_analysis_context(self):
        """
        Combines pandas analysis into a text dictionary/string 
        to be injected into the LLM prompt.
        """
        if not self.load_data():
            return "Failed to load data."
            
        context = {
            "Data Meta": self.get_summary_statistics(),
            "Regional Performance": self.get_performance_by_region(),
            "Product Performance": self.get_performance_by_product()
        }
        
        return context
