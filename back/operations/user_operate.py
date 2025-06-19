from django.contrib.auth.models import User


async def check_username_exist(username):
    """检查数据库里是否有该用户名
        存在就返回该用户，否则返回None
    """
    try:
        user = await User.objects.aget(username=username)
        return user
    except User.DoesNotExist as e:
        return None
