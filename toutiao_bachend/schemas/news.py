from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, ConfigDict, Field


class NewsListItem(BaseModel):
    """新闻列表项模型：供新闻列表、收藏列表等场景复用"""
    model_config = ConfigDict(populate_by_name=True)

    id: int
    title: str
    description: Optional[str] = None
    image: Optional[str] = None
    author: Optional[str] = None
    views: int = 0
    publish_time: datetime = Field(..., alias="publishTime")


class RelatedNewsItem(BaseModel):
    """相关新闻项模型：详情页展示用"""
    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

    id: int
    title: str
    content: str
    image: Optional[str] = None
    author: Optional[str] = None
    publish_time: datetime = Field(..., alias="publishTime")
    category_id: int = Field(..., alias="categoryId")
    views: int = 0


class NewsDetailResponse(BaseModel):
    """新闻详情响应模型"""
    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

    id: int
    title: str
    content: str
    image: Optional[str] = None
    author: Optional[str] = None
    publish_time: datetime = Field(..., alias="publishTime")
    category_id: int = Field(..., alias="categoryId")
    views: int = 0
    related_news: List[RelatedNewsItem] = Field(..., alias="relatedNews")
