import pandas as pd
import numpy as np
import os
import random
from datetime import datetime, timedelta

def generate_sample_sales_data(filepath='data/sample_sales.xlsx'):
    # Create data directory if it doesn't exist
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    np.random.seed(42)
    random.seed(42)
    
    dates = [datetime(2023, 1, 1) + timedelta(days=i) for i in range(100)]
    regions = ['North', 'South', 'East', 'West']
    products = ['Laptop', 'Smartphone', 'Tablet', 'Monitor']
    
    data = []
    for _ in range(500):
        date = random.choice(dates)
        region = random.choice(regions)
        product = random.choice(products)
        units_sold = random.randint(1, 50)
        
        # Base prices
        price_map = {'Laptop': 1200, 'Smartphone': 800, 'Tablet': 400, 'Monitor': 300}
        unit_price = price_map[product]
        
        # Add some random variance to price
        variance = random.uniform(0.9, 1.1)
        actual_price = round(unit_price * variance, 2)
        
        sales_revenue = units_sold * actual_price
        
        # Calculate profit margin (random between 10% and 30%)
        margin = random.uniform(0.1, 0.3)
        profit = round(sales_revenue * margin, 2)
        
        data.append({
            'Date': date,
            'Region': region,
            'Product': product,
            'Units Sold': units_sold,
            'Unit Price': actual_price,
            'Sales Revenue': sales_revenue,
            'Profit': profit
        })
        
    df = pd.DataFrame(data)
    
    # Sort by date
    df = df.sort_values(by='Date')
    
    # Save to Excel
    df.to_excel(filepath, index=False)
    print(f"Sample data generated successfully at: {filepath}")

if __name__ == "__main__":
    generate_sample_sales_data()
