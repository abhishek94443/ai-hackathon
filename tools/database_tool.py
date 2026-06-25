from langchain.tools import tool
from database.duckdb_manager import DuckDBManager

@tool("query_database")
def query_database(query: str) -> str:
    """
    Execute SQL queries against the DuckDB database.
    Useful for retrieving chat history, analysis results, or structured data.
    
    Args:
        query (str): The SQL query to execute.
        
    Returns:
        str: String representation of the query results (DataFrame).
    """
    try:
        manager = DuckDBManager()
        df = manager.execute_query(query)
        if df.empty:
            return "Query returned no results."
        return df.to_string()
    except Exception as e:
        return f"Error executing database query: {str(e)}"
