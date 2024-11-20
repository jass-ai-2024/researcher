"""
Data models for arxiv
"""
from pydantic import BaseModel, Field
from typing import Optional


class ArxivQuery(BaseModel):
    """Simple ArXiv query structure"""
    title: Optional[str] = Field(
        None,
        description="Search in title (ti:)",
        example='ti:"machine learning"'
    )

    #abstract: Optional[str] = Field(
    #    None,
    #    description="Search in abstract (abs:)",
    #    example='abs:"neural networks"'
    #)

    author: Optional[str] = Field(
        None,
        description="Search by author (au:)",
        example='au:"Hinton"'
    )

    category: Optional[str] = Field(
        None,
        description="Search by category (cat:)",
        example='cat:cs.AI'
    )

    date_range: Optional[str] = Field(
        None,
        description="Date range [YYYYMMDD TO YYYYMMDD]",
        example='submittedDate:[20230101 TO 20240101]'
    )

class Paper(BaseModel):
    """Paper metadata structure"""
    title: str
    semantic_score: float
    summary: str
    link: str
    authors: list[str]