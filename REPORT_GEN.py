import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from fpdf import FPDF
from datetime import datetime, timedelta
import json
import csv
import os
from io import BytesIO
import base64

class AutomatedReportGenerator:
    def __init__(self):
        self.data = None
        self.analysis_results = {}
        self.charts_path = "temp_charts/"
        self.ensure_charts_directory()
    
    def ensure_charts_directory(self):
        """Create charts directory if it doesn't exist"""
        if not os.path.exists(self.charts_path):
            os.makedirs(self.charts_path)
    
    def load_data(self, file_path, file_type='auto'):
        """Load data from various file formats"""
        try:
            if file_type == 'auto':
                file_type = file_path.split('.')[-1].lower()
            
            if file_type in ['csv']:
                self.data = pd.read_csv(file_path)
            elif file_type in ['xlsx', 'xls']:
                self.data = pd.read_excel(file_path)
            elif file_type == 'json':
                with open(file_path, 'r') as f:
                    json_data = json.load(f)
                self.data = pd.DataFrame(json_data)
            else:
                raise ValueError(f"Unsupported file type: {file_type}")
            
            print(f"Data loaded successfully: {len(self.data)} rows, {len(self.data.columns)} columns")
            return True
            
        except Exception as e:
            print(f"Error loading data: {e}")
            return False
    
    def analyze_data(self):
        """Perform comprehensive data analysis"""
        if self.data is None:
            print("No data loaded for analysis")
            return False
        
        # Basic statistics
        self.analysis_results['basic_stats'] = {
            'total_rows': len(self.data),
            'total_columns': len(self.data.columns),
            'missing_values': self.data.isnull().sum().sum(),
            'data_types': self.data.dtypes.to_dict()
        }
        
        # Numerical analysis
        numeric_columns = self.data.select_dtypes(include=[np.number]).columns
        if len(numeric_columns) > 0:
            self.analysis_results['numeric_summary'] = self.data[numeric_columns].describe()
            self.analysis_results['correlations'] = self.data[numeric_columns].corr()
        
        # Categorical analysis
        categorical_columns = self.data.select_dtypes(include=['object']).columns
        if len(categorical_columns) > 0:
            self.analysis_results['categorical_summary'] = {}
            for col in categorical_columns:
                self.analysis_results['categorical_summary'][col] = {
                    'unique_values': self.data[col].nunique(),
                    'top_values': self.data[col].value_counts().head(5).to_dict()
                }
        
        return True
    
    def generate_charts(self):
        """Generate various charts for the report"""
        if self.data is None:
            return []
        
        chart_files = []
        plt.style.use('seaborn-v0_8')
        
        # Chart 1: Data Overview
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        fig.suptitle('Data Overview Dashboard', fontsize=16, fontweight='bold')
        
        # Missing values heatmap
        if self.data.isnull().sum().sum() > 0:
            sns.heatmap(self.data.isnull(), cbar=True, ax=axes[0,0])
            axes[0,0].set_title('Missing Values Pattern')
        else:
            axes[0,0].text(0.5, 0.5, 'No Missing Values', ha='center', va='center', fontsize=14)
            axes[0,0].set_title('Missing Values Pattern')
        
        # Data types distribution
        dtype_counts = self.data.dtypes.value_counts()
        axes[0,1].pie(dtype_counts.values, labels=dtype_counts.index, autopct='%1.1f%%')
        axes[0,1].set_title('Data Types Distribution')
        
        # Numeric columns distribution
        numeric_cols = self.data.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            self.data[numeric_cols[:4]].hist(ax=axes[1,0], bins=20, alpha=0.7)
            axes[1,0].set_title('Numeric Distributions')
        
        # Sample data preview
        axes[1,1].axis('tight')
        axes[1,1].axis('off')
        table_data = self.data.head(5).round(2) if len(self.data) > 0 else pd.DataFrame()
        table = axes[1,1].table(cellText=table_data.values,
                               colLabels=table_data.columns,
                               cellLoc='center',
                               loc='center')
        table.auto_set_font_size(False)
        table.set_fontsize(8)
        axes[1,1].set_title('Data Sample')
        
        plt.tight_layout()
        chart1_path = f"{self.charts_path}overview_dashboard.png"
        plt.savefig(chart1_path, dpi=300, bbox_inches='tight')
        plt.close()
        chart_files.append(chart1_path)
        
        # Chart 2: Correlation Matrix (if numeric data exists)
        if len(numeric_cols) > 1:
            plt.figure(figsize=(10, 8))
            correlation_matrix = self.data[numeric_cols].corr()
            sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0,
                       square=True, fmt='.2f')
            plt.title('Correlation Matrix', fontsize=16, fontweight='bold')
            plt.tight_layout()
            chart2_path = f"{self.charts_path}correlation_matrix.png"
            plt.savefig(chart2_path, dpi=300, bbox_inches='tight')
            plt.close()
            chart_files.append(chart2_path)
        
        # Chart 3: Top Categories (if categorical data exists)
        categorical_cols = self.data.select_dtypes(include=['object']).columns
        if len(categorical_cols) > 0:
            fig, axes = plt.subplots(2, 2, figsize=(12, 10))
            fig.suptitle('Categorical Data Analysis', fontsize=16, fontweight='bold')
            
            for i, col in enumerate(categorical_cols[:4]):
                row, col_idx = i // 2, i % 2
                top_values = self.data[col].value_counts().head(10)
                top_values.plot(kind='bar', ax=axes[row, col_idx])
                axes[row, col_idx].set_title(f'Top Values in {col}')
                axes[row, col_idx].tick_params(axis='x', rotation=45)
            
            # Hide unused subplots
            for i in range(len(categorical_cols), 4):
                row, col_idx = i // 2, i % 2
                axes[row, col_idx].axis('off')
            
            plt.tight_layout()
            chart3_path = f"{self.charts_path}categorical_analysis.png"
            plt.savefig(chart3_path, dpi=300, bbox_inches='tight')
            plt.close()
            chart_files.append(chart3_path)
        
        return chart_files
    
    def generate_pdf_report(self, output_path="automated_report.pdf", report_title="Data Analysis Report"):
        """Generate comprehensive PDF report using FPDF"""
        
        # Generate charts
        chart_files = self.generate_charts()
        
        # Create PDF
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        
        # Title page
        pdf.add_page()
        pdf.set_font('Arial', 'B', 24)
        pdf.cell(0, 30, report_title, 0, 1, 'C')
        
        pdf.set_font('Arial', '', 12)
        pdf.cell(0, 10, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 0, 1, 'C')
        pdf.cell(0, 10, f"Generated by: PhantomX256", 0, 1, 'C')
        
        # Executive Summary
        pdf.ln(20)
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 10, 'Executive Summary', 0, 1, 'L')
        pdf.set_font('Arial', '', 12)
        
        summary_text = f"""
This automated report provides a comprehensive analysis of the loaded dataset containing 
{self.analysis_results.get('basic_stats', {}).get('total_rows', 'N/A')} rows and 
{self.analysis_results.get('basic_stats', {}).get('total_columns', 'N/A')} columns.

Key findings include statistical summaries, correlation analysis, and categorical 
breakdowns. The analysis reveals patterns and insights that can inform business 
decisions and data-driven strategies.
        """
        
        # Split text into lines for PDF
        lines = summary_text.strip().split('\n')
        for line in lines:
            if line.strip():
                pdf.cell(0, 6, line.strip(), 0, 1, 'L')
        
        # Data Overview Section
        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 10, 'Data Overview', 0, 1, 'L')
        
        basic_stats = self.analysis_results.get('basic_stats', {})
        pdf.set_font('Arial', '', 12)
        pdf.cell(0, 8, f"Total Rows: {basic_stats.get('total_rows', 'N/A')}", 0, 1, 'L')
        pdf.cell(0, 8, f"Total Columns: {basic_stats.get('total_columns', 'N/A')}", 0, 1, 'L')
        pdf.cell(0, 8, f"Missing Values: {basic_stats.get('missing_values', 'N/A')}", 0, 1, 'L')
        
        # Add charts
        for i, chart_path in enumerate(chart_files):
            if os.path.exists(chart_path):
                if i > 0:  # Add new page for subsequent charts
                    pdf.add_page()
                
                pdf.set_font('Arial', 'B', 14)
                chart_title = os.path.basename(chart_path).replace('.png', '').replace('_', ' ').title()
                pdf.cell(0, 10, chart_title, 0, 1, 'L')
                
                # Add image
                try:
                    pdf.image(chart_path, x=10, y=pdf.get_y()+5, w=190)
                except:
                    pdf.cell(0, 10, f"Chart could not be loaded: {chart_path}", 0, 1, 'L')
        
        # Statistical Summary
        if 'numeric_summary' in self.analysis_results:
            pdf.add_page()
            pdf.set_font('Arial', 'B', 16)
            pdf.cell(0, 10, 'Statistical Summary', 0, 1, 'L')
            
            pdf.set_font('Arial', '', 10)
            summary_df = self.analysis_results['numeric_summary']
            
            # Create a simple table
            for col in summary_df.columns[:3]:  # Show first 3 numeric columns
                pdf.ln(5)
                pdf.set_font('Arial', 'B', 12)
                pdf.cell(0, 8, f"Column: {col}", 0, 1, 'L')
                pdf.set_font('Arial', '', 10)
                
                for stat in ['mean', 'std', 'min', 'max']:
                    if stat in summary_df.index:
                        value = summary_df.loc[stat, col]
                        pdf.cell(0, 6, f"{stat.title()}: {value:.2f}", 0, 1, 'L')
        
        # Save PDF
        pdf.output(output_path)
        print(f"Report generated successfully: {output_path}")
        
        # Clean up temporary chart files
        for chart_path in chart_files:
            if os.path.exists(chart_path):
                os.remove(chart_path)
        
        return output_path

def main():
    """Main function to demonstrate the report generator"""
    print("Automated Report Generator")
    print("=" * 40)
    
    # Get file path from user
    file_path = input("Enter the path to your data file (CSV, Excel, or JSON): ").strip()
    
    if not file_path or not os.path.exists(file_path):
        print("Creating sample data for demonstration...")
        create_sample_data()
        file_path = "sample_sales_data.csv"
    
    # Initialize generator
    generator = AutomatedReportGenerator()
    
    # Load and analyze data
    if generator.load_data(file_path):
        generator.analyze_data()
        
        # Generate report
        report_title = input("Enter report title (or press Enter for default): ").strip()
        if not report_title:
            report_title = "Automated Data Analysis Report"
        
        output_file = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        generator.generate_pdf_report(output_file, report_title)
        
        print(f"\nReport generated: {output_file}")
    else:
        print("Failed to load data. Please check your file path and format.")

def create_sample_data():
    """Create sample data for demonstration"""
    np.random.seed(42)
    
    # Generate sample sales data
    dates = pd.date_range('2024-01-01', periods=365, freq='D')
    products = ['Product A', 'Product B', 'Product C', 'Product D', 'Product E']
    regions = ['North', 'South', 'East', 'West']
    
    data = []
    for _ in range(1000):
        data.append({
            'Date': np.random.choice(dates),
            'Product': np.random.choice(products),
            'Region': np.random.choice(regions),
            'Sales_Amount': np.random.normal(1000, 300),
            'Quantity': np.random.randint(1, 50),
            'Customer_Age': np.random.randint(18, 80),
            'Customer_Satisfaction': np.random.uniform(1, 5)
        })
    
    df = pd.DataFrame(data)
    df['Sales_Amount'] = df['Sales_Amount'].clip(lower=0)  # No negative sales
    df.to_csv('sample_sales_data.csv', index=False)
    print("Sample data created: sample_sales_data.csv")

if __name__ == "__main__":
    main()