import duckdb
import os
import pandas as pd
from typing import List, Dict, Any

class DuckDBManager:
    def __init__(self, db_path: str = "./data/hackathon.duckdb"):
        self.db_path = db_path
        # Ensure directory exists
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._initialize_tables()

    def _get_connection(self):
        return duckdb.connect(self.db_path)

    def _initialize_tables(self):
        """Creates basic tables for the hackathon application."""
        create_chat_sequence = "CREATE SEQUENCE IF NOT EXISTS seq_chat_id START 1;"
        create_chat_history = """
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY DEFAULT nextval('seq_chat_id'),
            role VARCHAR,
            content TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        
        create_analysis_sequence = "CREATE SEQUENCE IF NOT EXISTS seq_analysis_id START 1;"
        create_analysis_results = """
        CREATE TABLE IF NOT EXISTS analysis_results (
            id INTEGER PRIMARY KEY DEFAULT nextval('seq_analysis_id'),
            summary TEXT,
            confidence_score DOUBLE,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """

        with self._get_connection() as con:
            con.execute(create_chat_sequence)
            con.execute(create_analysis_sequence)
            con.execute(create_chat_history)
            con.execute(create_analysis_results)

    def execute_query(self, query: str) -> pd.DataFrame:
        """Executes a SQL query and returns results as a pandas DataFrame."""
        try:
            with self._get_connection() as con:
                return con.execute(query).df()
        except Exception as e:
            raise RuntimeError(f"DuckDB query error: {str(e)}")

    def store_chat_message(self, role: str, content: str):
        """Stores a chat message."""
        try:
            with self._get_connection() as con:
                con.execute(
                    "INSERT INTO chat_history (role, content) VALUES (?, ?)", 
                    [role, content]
                )
        except Exception as e:
            raise RuntimeError(f"Error storing chat message: {str(e)}")
            
    def store_analysis_result(self, summary: str, confidence_score: float):
        """Stores an analysis result."""
        try:
            with self._get_connection() as con:
                con.execute(
                    "INSERT INTO analysis_results (summary, confidence_score) VALUES (?, ?)", 
                    [summary, confidence_score]
                )
        except Exception as e:
            raise RuntimeError(f"Error storing analysis result: {str(e)}")
