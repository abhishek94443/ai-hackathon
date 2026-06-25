from pydantic import BaseModel, Field
from typing import List

class AnalysisResult(BaseModel):
    """Structured output for data analysis results."""
    summary: str = Field(description="A brief summary of the analysis.")
    key_findings: List[str] = Field(description="List of key findings from the analysis.")
    risks: List[str] = Field(description="Potential risks or issues identified.")
    recommendations: List[str] = Field(description="Actionable recommendations based on the findings.")
    confidence_score: float = Field(description="Confidence score of the analysis between 0.0 and 1.0.")
