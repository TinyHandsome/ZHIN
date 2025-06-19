from typing import Optional
from ninja import Schema


class OutCommonResponse(Schema):
    """通用响应格式"""

    status: int
    msg: str
    data: Optional[dict] = None


def get_success_response(msg="success", status=1, *args, **kwargs):
    """正常返回的模板"""
    temp = {"status": status, "msg": msg}
    if kwargs:
        temp.update({"data": kwargs})
    return temp


def get_error_response(msg="error", status=0, *args, **kwargs):
    """错误返回的模板"""
    temp = {"status": status, "msg": msg}
    if kwargs:
        temp.update({"data": kwargs})
    return temp
