# ============================================================
# 数据访问层（crud 层）：与数据库交互的唯一出口
# ============================================================
# 模块清单：
# - users.py     user / user_token 表：查询、创建、更新
# - news.py      news_category / news 表：查询、浏览量自增
# - favorite.py  favorite 表：增删查清、收藏 join 新闻联查
# - history.py   history 表：增删查清、历史 join 新闻联查
#
# 设计约束（"纯数据访问"的判定标准）：
# 1. 每个函数 = 一组纯 SQL 操作，参数是裸值，不收 Schema 对象
# 2. 不 import HTTPException：业务错误由 services 层抛出
# 3. 不组装 Pydantic 模型：返回 ORM 实体或原始行，组装交给 services
# 4. 写操作内部自行 commit；读操作不 commit
