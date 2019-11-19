from channels.routing import ProtocolTypeRouter, URLRouter
import insta.routing
from channels.auth import AuthMiddlewareStack

application = ProtocolTypeRouter({
     # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
         URLRouter(
            insta.routing.websocket_urlpatterns
        )
     ),
})