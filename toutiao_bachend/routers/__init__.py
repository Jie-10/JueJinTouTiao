# ============================================================
# 接口层（router 层）：对外暴露 HTTP API
# ============================================================
# 模块清单：news / users / favorite / history
# 由 main.py 通过 app.include_router 统一挂载（前缀 /api/xxx）
#
# 每个路由函数的职责边界（只做四件事）：
# 1. 声明路径、方法与请求参数（含 Query(alias=...) 驼峰键映射）
# 2. 通过 Depends 注入依赖（get_db 数据库会话、get_current_user 当前用户）
# 3. 调用一个 service 函数完成业务，并拿到业务结果
# 4. 用 success_response 包装统一响应 {code, message, data}
#
# 边界约束：不写业务判断、不写 SQL、不组装复杂数据结构
