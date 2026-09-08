import json

from django.core.serializers.json import DjangoJSONEncoder
from django.db import transaction
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from ..model.hieusuat import ChiSoHieuSuat
from ..model.lienket import LienKet
from ..model.lohong import LoHong
from ..model.nhanvien import NhanVien
from ..model.nhatkyloi import NhatKyLoi
from ..model.thietbi import ThietBi
from ..utils.sql_error_handler import get_sql_error

IMPORT_EXPORT_FORMAT = settings.IMPORT_EXPORT_FORMAT
IMPORT_EXPORT_VERSION = settings.IMPORT_EXPORT_VERSION

IMPORT_EXPORT_MODELS = {
    "nhanvien": NhanVien,
    "thietbi": ThietBi,
    "lienket": LienKet,
    "hieusuat": ChiSoHieuSuat,
    "lohong": LoHong,
    "nhatkyloi": NhatKyLoi,
}


def get_model(model_name):
    """Hàm get model để lấy bảng dữ liệu cho export"""
    model = IMPORT_EXPORT_MODELS.get(model_name)

    if model is None:
        raise ValueError(f"Model '{model_name}' không được hỗ trợ.")

    return model


""" =================== EXPORT =================== """


def export_model(model_name):
    model = get_model(model_name)

    records = []

    for instance in model.objects.all():
        record = {}

        for field in model._meta.concrete_fields:
            record[field.name] = getattr(
                instance,
                field.attname,
            )

        records.append(record)

    return {
        "format": IMPORT_EXPORT_FORMAT,
        "version": IMPORT_EXPORT_VERSION,
        "model": model_name,
        "records": records,
    }


def export_model_to_json(model_name):
    return json.dumps(
        export_model(model_name),
        cls=DjangoJSONEncoder,
        ensure_ascii=False,
        indent=2,
    )


def export_model_response(model_name):
    """Export dữ liệu model thành file JSON."""
    try:
        json_data = export_model_to_json(model_name)

        response = HttpResponse(
            json_data,
            content_type="application/json; charset=utf-8",
        )

        response["Content-Disposition"] = (
            f'attachment; filename="{model_name}_export.json"'
        )

        return response

    except ValueError as e:
        message, status_code = get_sql_error(e)
        return JsonResponse({"error": message}, status=400)

    except Exception as e:
        message, status_code = get_sql_error(e)
        return JsonResponse({"error": message}, status=status_code)


# =========================================================
# IMPORT
# =========================================================


def validate_import_data(payload, model_name):
    if not isinstance(payload, dict):
        raise ValueError("Dữ liệu import phải là một object JSON.")

    if payload.get("format") != IMPORT_EXPORT_FORMAT:
        raise ValueError("Định dạng file import không được hỗ trợ.")

    if payload.get("version") != IMPORT_EXPORT_VERSION:
        raise ValueError("Phiên bản file import không được hỗ trợ.")

    if payload.get("model") != model_name:
        raise ValueError("Model trong file import không khớp với API.")

    records = payload.get("records")

    if not isinstance(records, list):
        raise ValueError("Trường 'records' phải là một danh sách.")

    model = get_model(model_name)

    field_names = {field.name for field in model._meta.concrete_fields}

    for index, record in enumerate(records):

        if not isinstance(record, dict):
            raise ValueError(f"Bản ghi thứ {index + 1} không hợp lệ.")

        unknown_fields = set(record.keys()) - field_names

        if unknown_fields:
            raise ValueError(
                f"Bản ghi thứ {index + 1} chứa "
                f"trường không được hỗ trợ: " + ", ".join(sorted(unknown_fields))
            )


@transaction.atomic
def import_model(model_name, payload):
    """
    Import dữ liệu vào model.

    Nếu PK đã tồn tại:
        UPDATE

    Nếu PK chưa tồn tại:
        CREATE

    Không xóa dữ liệu cũ.
    """

    validate_import_data(
        payload,
        model_name,
    )

    model = get_model(model_name)

    primary_key = model._meta.pk.name

    created_count = 0
    updated_count = 0

    records = payload["records"]

    for record in records:

        values = {}

        for field in model._meta.concrete_fields:

            if field.name not in record:
                continue

            try:
                values[field.name] = field.to_python(record[field.name])

            except (TypeError, ValueError) as exc:
                raise ValueError(
                    f"Giá trị trường "
                    f"'{field.name}' "
                    f"của model "
                    f"'{model_name}' "
                    f"không hợp lệ."
                ) from exc

        if primary_key not in values:
            raise ValueError(f"Bản ghi thiếu khóa chính " f"'{primary_key}'.")

        primary_key_value = values.pop(primary_key)

        _, created = model.objects.update_or_create(
            **{
                primary_key: primary_key_value,
            },
            defaults=values,
        )

        if created:
            created_count += 1
        else:
            updated_count += 1

    return {
        "model": model_name,
        "total": len(records),
        "created": created_count,
        "updated": updated_count,
    }


def import_model_response(request, model_name):
    """
    Import file JSON được upload từ Postman.
    """

    try:
        # -------------------------------------------------
        # Kiểm tra model
        # -------------------------------------------------

        get_model(model_name)

        # -------------------------------------------------
        # Kiểm tra file
        # -------------------------------------------------

        uploaded_file = request.FILES.get("file")

        if uploaded_file is None:
            raise ValueError("Vui lòng upload file JSON với key 'file'.")

        # -------------------------------------------------
        # Kiểm tra extension
        # -------------------------------------------------

        if not uploaded_file.name.lower().endswith(".json"):
            raise ValueError("File import phải có định dạng .json.")

        # -------------------------------------------------
        # Đọc file
        # -------------------------------------------------

        try:
            file_content = uploaded_file.read()

            payload = json.loads(file_content.decode("utf-8"))

        except UnicodeDecodeError as exc:
            raise ValueError("File JSON phải sử dụng encoding UTF-8.") from exc

        except json.JSONDecodeError as exc:
            raise ValueError("File không phải JSON hợp lệ.") from exc

        # -------------------------------------------------
        # Import
        # -------------------------------------------------

        result = import_model(
            model_name,
            payload,
        )

        return JsonResponse(
            {
                "message": (f"Import dữ liệu " f"{model_name} " f"thành công."),
                "data": result,
            },
            status=200,
        )

    except ValueError as e:
        message, status_code = get_sql_error(e)
        return JsonResponse({"error": message}, status=400)

    except Exception as e:
        message, status_code = get_sql_error(e)
        return JsonResponse({"error": message}, status=status_code)
