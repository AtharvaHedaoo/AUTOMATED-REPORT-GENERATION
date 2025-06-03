import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json

def create_sales_data():
    """Create comprehensive sales data"""
    np.random.seed(42)
    
    # Generate date range
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2024, 12, 31)
    date_range = pd.date_range(start_date, end_date, freq='D')
    
    products = ['Laptop', 'Desktop', 'Monitor', 'Keyboard', 'Mouse', 'Headphones', 'Webcam', 'Tablet']
    categories = ['Electronics', 'Accessories', 'Computing', 'Audio']
    regions = ['North America', 'Europe', 'Asia Pacific', 'Latin America']
    sales_channels = ['Online', 'Retail', 'Partner', 'Direct']
    
    data = []
    for _ in range(2000):
        product = np.random.choice(products)
        base_price = {
            'Laptop': 1200, 'Desktop': 800, 'Monitor': 300, 'Keyboard': 50,
            'Mouse': 25, 'Headphones': 100, 'Webcam': 75, 'Tablet': 400
        }[product]
        
        data.append({
            'Date': np.random.choice(date_range),
            'Product': product,
            'Category': np.random.choice(categories),
            'Region': np.random.choice(regions),
            'Sales_Channel': np.random.choice(sales_channels),
            'Unit_Price': base_price * np.random.uniform(0.8, 1.3),
            'Quantity_Sold': np.random.randint(1, 20),
            'Discount_Percent': np.random.uniform(0, 0.3),
            'Customer_Rating': np.random.uniform(3.0, 5.0),
            'Shipping_Cost': np.random.uniform(5, 50),
            'Marketing_Spend': np.random.uniform(10, 500)
        })
    
    df = pd.DataFrame(data)
    
    # Calculate derived columns
    df['Revenue'] = df['Unit_Price'] * df['Quantity_Sold'] * (1 - df['Discount_Percent'])
    df['Profit_Margin'] = np.random.uniform(0.1, 0.4, len(df))
    df['Profit'] = df['Revenue'] * df['Profit_Margin']
    df['Month'] = df['Date'].dt.month
    df['Quarter'] = df['Date'].dt.quarter
    df['Day_of_Week'] = df['Date'].dt.day_name()
    
    return df

def create_hr_data():
    """Create HR analytics data"""
    np.random.seed(123)
    
    departments = ['Engineering', 'Sales', 'Marketing', 'HR', 'Finance', 'Operations']
    job_levels = ['Junior', 'Mid', 'Senior', 'Lead', 'Manager', 'Director']
    education = ['High School', 'Bachelor', 'Master', 'PhD']
    
    data = []
    for i in range(800):
        dept = np.random.choice(departments)
        level = np.random.choice(job_levels)
        
        # Base salary by department and level
        base_salaries = {
            'Engineering': {'Junior': 70000, 'Mid': 90000, 'Senior': 120000, 'Lead': 140000, 'Manager': 160000, 'Director': 200000},
            'Sales': {'Junior': 50000, 'Mid': 70000, 'Senior': 90000, 'Lead': 110000, 'Manager': 130000, 'Director': 180000},
            'Marketing': {'Junior': 55000, 'Mid': 75000, 'Senior': 95000, 'Lead': 115000, 'Manager': 135000, 'Director': 175000},
            'HR': {'Junior': 50000, 'Mid': 65000, 'Senior': 85000, 'Lead': 105000, 'Manager': 125000, 'Director': 160000},
            'Finance': {'Junior': 60000, 'Mid': 80000, 'Senior': 100000, 'Lead': 120000, 'Manager': 140000, 'Director': 190000},
            'Operations': {'Junior': 55000, 'Mid': 70000, 'Senior': 90000, 'Lead': 110000, 'Manager': 130000, 'Director': 170000}
        }
        
        base_salary = base_salaries[dept][level]
        
        data.append({
            'Employee_ID': f"EMP_{i+1:04d}",
            'Department': dept,
            'Job_Level': level,
            'Education': np.random.choice(education),
            'Years_Experience': np.random.randint(0, 25),
            'Age': np.random.randint(22, 65),
            'Salary': base_salary * np.random.uniform(0.9, 1.2),
            'Performance_Rating': np.random.uniform(2.5, 5.0),
            'Training_Hours_Annual': np.random.randint(0, 120),
            'Overtime_Hours_Monthly': np.random.randint(0, 40),
            'Sick_Days_Annual': np.random.randint(0, 15),
            'Employee_Satisfaction': np.random.uniform(2.0, 5.0),
            'Years_at_Company': np.random.randint(0, 20),
            'Remote_Work_Days': np.random.randint(0, 5)
        })
    
    return pd.DataFrame(data)

def save_sample_datasets():
    """Save multiple sample datasets"""
    
    # Sales data
    sales_df = create_sales_data()
    sales_df.to_csv('sample_sales_comprehensive.csv', index=False)
    sales_df.to_excel('sample_sales_comprehensive.xlsx', index=False)
    
    # HR data
    hr_df = create_hr_data()
    hr_df.to_csv('sample_hr_analytics.csv', index=False)
    
    # JSON format
    sales_json = sales_df.head(100).to_dict('records')
    with open('sample_sales_data.json', 'w') as f:
        json.dump(sales_json, f, indent=2, default=str)
    
    print("Sample datasets created:")
    print("- sample_sales_comprehensive.csv")
    print("- sample_sales_comprehensive.xlsx") 
    print("- sample_hr_analytics.csv")
    print("- sample_sales_data.json")

if __name__ == "__main__":
    save_sample_datasets()