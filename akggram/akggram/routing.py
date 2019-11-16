# from channels.routing import ProtocolTypeRouter
# from channels.security.websocket import AllowedHostsOriginValidator,OriginValidator
# from channels.auth import AuthMiddleware
# from channels.routing import ProtocolTypeRouter, URLRouter
# from django.conf.urls import url
# from insta.consumer import ChatConsumer


# application = ProtocolTypeRouter({
#     # Empty for now (http->django views is added by default)
#     'websocket': AllowedHostsOriginValidator(
#         AuthMiddleware(
#             URLRouter(
#                 [
#                  url(r"^(?P<username>[\w.@+-]+)/$", ChatConsumer),
#                 ]
#             )


#         )

#     )
# })