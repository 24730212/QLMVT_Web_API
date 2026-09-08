from rest_framework.decorators import (
    api_view,
    permission_classes,
)

from ..permission.permission import IsAdmin

from ..controller.import_export import (
    export_model_response,
    import_model_response,
)


@api_view(["GET"])
@permission_classes([IsAdmin])
def api_export_table(request, model_name):
    return export_model_response(model_name)


@api_view(["POST"])
@permission_classes([IsAdmin])
def api_import_table(request, model_name):
    return import_model_response(
        request,
        model_name,
    )
