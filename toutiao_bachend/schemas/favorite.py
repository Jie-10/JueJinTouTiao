from datetime import datetime

from pydantic import BaseModel, ConfigDict
from pydantic import Field

from schemas.news import NewsListItem


class FavoriteCheckResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    is_favorite: bool = Field(..., alias="isFavorite")

class FavoriteAddRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    news_id: int = Field(..., alias="newsId")

class FavoriteListItem(NewsListItem):
    """收藏列表项模型：复用新闻列表项字段，额外携带收藏时间"""

    favorite_time: datetime = Field(..., alias="favoriteTime")
