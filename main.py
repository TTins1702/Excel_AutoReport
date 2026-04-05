import os
import argparse
from generate_sample_data import generate_sample_sales_data
from data_analyzer import DataAnalyzer
from agent import ReportAgent

def main():
    parser = argparse.ArgumentParser(description="AI Agent for Excel Reporting")
    parser.add_argument("--file", type=str, default="data/sample_sales.xlsx", help="Path to the Excel file")
    parser.add_argument("--output", type=str, default="report.md", help="Path to save the generated report")
    parser.add_argument("--generate-sample", action="store_true", help="Generate sample data before running")
    args = parser.parse_args()

    # 1. Provide Context & Data
    if args.generate_sample or not os.path.exists(args.file):
        print("Generating sample data...")
        generate_sample_sales_data(args.file)
        
    print(f"\n--- Starting Analysis for {args.file} ---")
    
    # 2. Analyze Data with Pandas
    analyzer = DataAnalyzer(args.file)
    analysis_context = analyzer.generate_analysis_context()
    
    if isinstance(analysis_context, str) and analysis_context.startswith("Failed"):
        print("Exiting due to data loading failure.")
        return

    # 3. Generate Report using LLM Agent
    try:
        agent = ReportAgent()
        report_markdown = agent.generate_report(analysis_context)
        
        if report_markdown:
            # 4. Save and Output Report
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(report_markdown)
            print(f"\n[SUCCESS] Report generated successfully and saved to {args.output}")
            print("\nPreview of Report:\n")
            # Print the first 500 characters as preview
            print(report_markdown[:500] + "...\n")
        else:
            print("Failed to generate report.")
    except ValueError as e:
        print(f"\nConfiguration Error: {e}")
        print("Please check your .env file and ensure GROQ_API_KEY is correctly set.")

if __name__ == "__main__":
    main()
