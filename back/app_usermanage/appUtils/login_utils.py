import configs as CONFIG
import ldap3


def check_ldap_enabled():
    """检查是否启用LDAP验证"""
    return CONFIG.OPEN_LDAP and CONFIG.AUTH_LDAP_SERVER_URI != ""


def ldap_authenticate(username, password):
    """通过ldap验证用户是否存在"""
    # 构造 LDAP 服务器对象
    server = ldap3.Server(CONFIG.AUTH_LDAP_SERVER_URI)

    # 创建连接
    conn = ldap3.Connection(
        server,
        user=f"ap\\{username}",
        password=password,
        client_strategy=ldap3.ASYNC
    )
    # 如果绑定成功，返回 True
    return conn.bind()
