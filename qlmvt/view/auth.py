from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.permissions import AllowAny

from ..permission.permission import (
    IsAuthenticated,
    IsAdmin,
)
from ..controller import auth


@api_view(["POST"])
@authentication_classes([])
@permission_classes([AllowAny])
def api_login(request):
    return auth.login(request)


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def api_logout(request):
    return auth.logout(request)


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def api_me(request):
    return auth.get_me(request)


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdmin])
def api_create_account(request):
    return auth.create_account(request)


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def api_change_password(request):
    return auth.change_password(request)
