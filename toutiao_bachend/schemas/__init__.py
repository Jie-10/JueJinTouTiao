# ============================================================
# Pydantic 模型包：接口请求/响应数据结构
# ============================================================
# 模块清单：
# - users.py     用户相关：注册/登录入参、用户信息出参、更新入参、改密入参
# - news.py      新闻相关：列表项、相关新闻项、详情响应
# - favorite.py  收藏相关：检查出参、添加入参、列表项（复用 NewsListItem）
# - history.py   浏览历史：添加入参、列表项（复用 NewsListItem）
#
# 命名约定：
# - 入参模型后缀 Request，出参模型后缀 Response
# - 前端 JSON 键用驼峰：字段配 Field(alias="...")，并在
#   model_config 开 populate_by_name=True 实现双向兼容
# - 出参模型配 from_attributes=True，便于从 ORM 对象直接 model_validate
# - 响应类字段名用 Python 下划线，序列化时按 alias 输出驼峰键
