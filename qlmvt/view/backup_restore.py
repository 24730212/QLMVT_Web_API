from rest_framework.decorators import (
    api_view,
    permission_classes,
)

from ..permission.permission import IsAdmin

from ..controller.backup_restore import (
    backup_database,
    restore_database,
)


@api_view(["GET"])
@permission_classes([IsAdmin])
def api_backup_database(request):
    return backup_database()


@api_view(["POST"])
@permission_classes([IsAdmin])
def api_restore_database(request):
    return restore_database(request)
