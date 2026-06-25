from langchain.tools import tool
from database.duckdb_manager import DuckDBManager

@tool("analyze_data")
def analyze_data(query: str) -> str:
    """
    Analyzes structured data and provides statistical insights.
    Useful when you need to perform numerical analysis on the database.
    
    Args:
        query (str): A SQL query that retrieves the data to analyze.
        
    Returns:
        str: The result of the analysis summary.
    """
    try:
        manager = DuckDBManager()
        df = manager.execute_query(query)
        if df.empty:
            return "No data available for analysis."
        
        # In a real scenario, this would use pandas to perform complex analysis
        summary = df.describe().to_string()
        return f"Analysis Summary:\n{summary}"
    except Exception as e:
        return f"Error performing data analysis: {str(e)}"
