# ============================================================
# ORM 模型包：数据库表结构的 Python 映射
# ============================================================
# 模块清单：
# - base.py     公共基类：DeclarativeBase（全项目唯一）与
#               TimestampMixin（created_at / updated_at 混入）
# - users.py    user 表、user_token 表
# - news.py     news_category 分类表、news 新闻表
# - favorite.py favorite 收藏表（user_id+news_id 联合唯一约束）
# - history.py  history 浏览历史表
#
# 重要约束：DeclarativeBase 只能在 base.py 定义一次，
# 所有模型统一继承 Base；若各模型文件各自定义基类，
# metadata 注册表相互独立，外键跨模型解析会失败
