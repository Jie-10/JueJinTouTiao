from datetime import datetime

from pydantic import BaseModel, ConfigDict
from pydantic import Field

from schemas.news import NewsListItem


class HistoryAddRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    news_id: int = Field(..., alias="newsId")


class HistoryListItem(NewsListItem):
    """浏览历史列表项模型：复用新闻列表项字段，额外携带浏览时间"""

    view_time: datetime = Field(..., alias="viewTime")
