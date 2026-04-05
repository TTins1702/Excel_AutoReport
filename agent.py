import os
import json
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ReportAgent:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key or api_key == "your_groq_api_key_here":
            raise ValueError("Invalid or missing GROQ_API_KEY. Please set it in the .env file.")
        
        self.client = Groq(api_key=api_key)
        # Using Llama 3.3 70B for fast and capable analysis on Groq
        self.model_id = 'llama-3.3-70b-versatile'

    def generate_report(self, analysis_context):
        """
        Takes the analytical context (from pandas) and uses Groq to generate a report.
        """
        context_str = json.dumps(analysis_context, indent=2)
        
        prompt = f"""
You are an expert Data Analyst and Business Consultant. 
I have extracted the following summarized data from a business Excel file.

### Data Summary:
{context_str}

### INSTRUCTIONS:
Please write a professional, comprehensive, and well-structured business report based on the provided data.
The report should include:
1. **Executive Summary**: A brief overview of the key performance indicators (KPIs) like total revenue and profit.
2. **Regional Analysis**: Breakdown of performance across different regions. Which region is performing best/worst?
3. **Product Performance**: Insights on the products sold. What is the top seller? What drives the revenue?
4. **Actionable Recommendations**: Give 2-3 strategic business recommendations based on the data trends.

Format the report using Markdown for easy readability (use headings, bullet points, and bold text).
Ensure the tone is professional, objective, and data-driven. Do NOT mention that you are an AI.
"""
        
        print(f"Sending analytical data to LLM ({self.model_id}) for report generation...")
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model=self.model_id,
                temperature=0.5,
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            print(f"Error during report generation: {e}")
            return None
