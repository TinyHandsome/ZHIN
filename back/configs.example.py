# SECTION 用户管理
# 是否打开注册，默认打开，开发者模式时关闭
# - 如果考虑 ladap 验证登录，那么可以不用打开注册
# - 如果考虑管理员自行添加用户，那么可以不用打开注册
OPEN_SIGNIN = True

# 是否打开Ldap，默认关闭
# - 打开：么用户登录验证失败之后，会自动去ldap验证
# - 关闭：登录验证失败就直接返回找不到用户
OPEN_LDAP = False
AUTH_LDAP_SERVER_URI = ""
