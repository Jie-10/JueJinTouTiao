# ============================================================
# 横切工具包：与业务无关的通用能力
# ============================================================
# 模块清单：
# - security.py            密码安全：bcrypt 哈希生成与校验
# - response.py            统一响应：success_response 生成 {code, message, data}
# - exception.py           异常处理器：HTTPException / IntegrityError /
#                          SQLAlchemyError / 未捕获异常（DEBUG_MODE 控制详情）
# - exception_handlers.py  把各处理器注册到 FastAPI app 的统一入口
# - auth.py                Web 层认证依赖 get_current_user：
#                          解析 Authorization 头 -> 调 service 校验 -> 返回用户
# - cache.py               Redis 底层封装：get / setex / delete / exists
#
# 边界划分（重要）：领域规则与 Web 适配分离——
# 认证依赖（utils/auth.py）只做 HTTP 适配，token 过期校验等
# 业务规则在 services/auth.py
