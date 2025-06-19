from ninja import NinjaAPI
from ninja.throttling import AuthRateThrottle
from ninja_jwt.controller import NinjaJWTDefaultController
from ninja_extra import NinjaExtraAPI
from django.contrib.admin.views.decorators import staff_member_required


api = NinjaExtraAPI(throttle=[AuthRateThrottle("5/1m")], docs_decorator=staff_member_required)
api.register_controllers(NinjaJWTDefaultController)

api.add_router("/usermanage/", "app_usermanage.api.router")
