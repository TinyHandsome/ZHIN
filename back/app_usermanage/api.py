import traceback
from ninja import Router, Schema
from ninja_jwt.authentication import JWTAuth
from ninja_jwt.tokens import RefreshToken
from ninja.throttling import AnonRateThrottle
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from asgiref.sync import sync_to_async

from app_usermanage.appUtils.login_utils import check_ldap_enabled, ldap_authenticate
import configs as CONFIG
from operations.user_operate import check_username_exist
from utils.response import OutCommonResponse, get_error_response, get_success_response

router = Router(tags=["用户管理"], auth=JWTAuth())


@router.get("/health", auth=None, response=OutCommonResponse)
def get_health(request):
    """检查 usermanage 服务是否健康"""
    return get_success_response(msg="App UserManage service is running.")


class InLoginSchema(Schema):
    username: str
    password: str


@router.post(
    "/login", auth=None, response=OutCommonResponse, throttle=[AnonRateThrottle("3/1m")]
)
async def login(request, data: InLoginSchema):
    """登录"""
    # 验证用户登录
    user = await sync_to_async(authenticate)(
        username=data.username, password=data.password
    )

    # INFO 如果不通过就检查ldap
    # INFO [user.is_active] 不用检查，因为 authenticate 已经检查过了
    if user is None:
        # print(f"> Password is incorrect for user {data.username}.")
        # 检查是否做LDAP
        if check_ldap_enabled():
            # 进行ldap验证
            is_ldap_user: bool = ldap_authenticate(data.username, data.password)
            # 如果ldap验证通过就创建用户，否则就验证失败
            if is_ldap_user:
                user = await check_username_exist(data.username)
                if user is not None:
                    # 系统里存在用户，修改密码
                    user.set_password(data.password)
                    await user.asave()
                    print(f"> <{data.username}>: 系统中已有同名用户，更新密码为ldap")
                else:
                    # 不存在该用户，创建新用户
                    try:
                        user = await User.objects.acreate_user(
                            data.username,
                            f"{data.username}@example.com",
                            data.password,
                            first_name=data.username,
                        )
                        print(f"> <{data.username}>: ldap验证通过，创建新用户成功")
                    except Exception as e:
                        print(f"> <{data.username}>: ldap验证通过，但创建用户失败")
                        traceback.print_exc()
                        return get_error_response(
                            msg="ldap验证通过，但创建用户失败",
                        )
            # LDAP 验证失败返回
            else:
                print(f"> <{data.username}>: 登录验证失败")
                return get_error_response(
                    msg="用户名或密码错误，或者该用户已过期", status=0
                )
        # 不开LDAP返回
        else:
            print(f"> <{data.username}>: 登录验证失败")
            return get_error_response(
                msg="用户名或密码错误，或者该用户已过期", status=0
            )

    # print(f"> Password is correct for user {data.username}.")
    refresh = RefreshToken.for_user(user)
    print(f"> <{data.username}>: 登录验证成功")
    return get_success_response(
        refresh=str(refresh), accessToken=str(refresh.access_token)
    )


class InSigninSchema(Schema):
    username: str
    password: str
    nickname: str = ""


@router.post("/signin", auth=None, response=OutCommonResponse)
async def signin(request, data: InSigninSchema):
    """注册"""
    if not CONFIG.OPEN_SIGNIN:
        # print("> The sign-in feature is not available.")
        return get_error_response(msg="注册功能未开启")

    # 检查用户是否存在
    try:
        user = await User.objects.aget(username=data.username)
        # print("> User already exists, cannot sign up again.")
        return get_error_response(msg="用户已存在，无法注册")
    except User.DoesNotExist as e:
        # print("> User does not exist, creating a new user.")
        user = await User.objects.acreate_user(
            username=data.username,
            email="{}@example.com".format(data.username),
            password=data.password,
            first_name=data.nickname if data.nickname else data.username,
        )
        return get_success_response(msg="注册成功", username=user.username)


@router.get("/info", response=OutCommonResponse, throttle=[AnonRateThrottle("30/1m")])
def get_user_info(request):
    """获取用户信息"""
    user: User = request.auth

    return get_success_response(
        userId=user.id,
        username=user.username,
        realName=user.first_name or user.username,
        # 头像
        avatar="",
        # 介绍
        decs=user.email,
        roles=[],
    )
