"""
Data models for arxiv
"""
from typing import Optional

from pydantic import BaseModel, Field


class ArxivQuery(BaseModel):
    """Simple ArXiv query structure"""
    all_fields: Optional[str] = Field(
        None,
        description="Search in all fields. Short and arXiv specific phrase. max 3-5 words",
        example='machine learning'
    )
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
