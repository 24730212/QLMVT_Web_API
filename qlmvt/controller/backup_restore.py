import json

from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder
from django.db import transaction
from django.http import HttpResponse, JsonResponse

from ..model.hieusuat import ChiSoHieuSuat
from ..model.lienket import LienKet
from ..model.lohong import LoHong
from ..model.nhanvien import NhanVien
from ..model.nhatkyloi import NhatKyLoi
from ..model.thietbi import ThietBi

from ..utils.sql_error_handler import get_sql_error

# =========================================================
# CONFIG
# =========================================================
BACKUP_FORMAT = settings.BACKUP_FORMAT
BACKUP_VERSION = settings.BACKUP_VERSION


# Phải restore bảng cha trước bảng có khóa ngoại.
BACKUP_MODELS = (
    ("nhanvien", NhanVien),
    ("thietbi", ThietBi),
    ("lienket", LienKet),
    ("hieusuat", ChiSoHieuSuat),
    ("lohong", LoHong),
    ("nhatkyloi", NhatKyLoi),
)


# =========================================================
# BACKUP
# =========================================================
def create_backup():
    """
    Tạo snapshot dữ liệu.

    Không thay đổi database.
    """

    models_data = {}

    for name, model in BACKUP_MODELS:

        records = []

        for instance in model.objects.all():

            record = {}

            for field in model._meta.concrete_fields:
                record[field.name] = getattr(
                    instance,
                    field.attname,
                )

            records.append(record)

        models_data[name] = records

    return {
        "format": BACKUP_FORMAT,
        "version": BACKUP_VERSION,
        "models": models_data,
    }


def backup_to_json():
    """
    Chuyển backup thành JSON.
    """

    return json.dumps(
        create_backup(),
        cls=DjangoJSONEncoder,
        ensure_ascii=False,
        indent=2,
    )


def backup_database():
    """
    Backup toàn bộ database được hỗ trợ
    thành file JSON.
    """

    try:
        json_data = backup_to_json()

        response = HttpResponse(
            json_data,
            content_type="application/json; charset=utf-8",
        )

        response["Content-Disposition"] = 'attachment; filename="qlmvt_backup.json"'

        return response

    except Exception as e:

        message, status_code = get_sql_error(e)

        return JsonResponse(
            {
                "error": message,
            },
            status=status_code,
        )


# =========================================================
# VALIDATE BACKUP
# =========================================================


def validate_backup(payload):
    """
    Kiểm tra file backup trước khi restore.
    """

    if not isinstance(payload, dict):
        raise ValueError("Dữ liệu backup phải là một object JSON.")

    if payload.get("format") != BACKUP_FORMAT:
        raise ValueError("Định dạng file backup không được hỗ trợ.")

    if payload.get("version") != BACKUP_VERSION:
        raise ValueError("Phiên bản file backup không được hỗ trợ.")

    models = payload.get("models")

    if not isinstance(models, dict):
        raise ValueError("File backup thiếu trường models.")

    supported_models = {name for name, _ in BACKUP_MODELS}

    unknown_models = set(models.keys()) - supported_models

    if unknown_models:
        raise ValueError(
            "File backup chứa model không được hỗ trợ: "
            + ", ".join(sorted(unknown_models))
        )

    for name, model in BACKUP_MODELS:

        records = models.get(name, [])

        if not isinstance(records, list):
            raise ValueError(f"Dữ liệu của model {name} phải là danh sách.")

        field_names = {field.name for field in model._meta.concrete_fields}

        for record in records:

            if not isinstance(record, dict):
                raise ValueError(f"Bản ghi của model {name} không hợp lệ.")

            unknown_fields = set(record.keys()) - field_names

            if unknown_fields:
                raise ValueError(
                    f"Bản ghi {name} chứa trường "
                    f"không được hỗ trợ: " + ", ".join(sorted(unknown_fields))
                )


# =========================================================
# RESTORE
# =========================================================


@transaction.atomic
def restore_backup(payload):
    """
    Restore database từ backup.

    - Record tồn tại -> update
    - Record chưa tồn tại -> create
    - Không xóa record hiện tại
    - Restore theo thứ tự khóa ngoại
    - Có lỗi -> rollback toàn bộ transaction
    """

    validate_backup(payload)

    restored = {}

    for name, model in BACKUP_MODELS:

        count = 0

        records = payload["models"].get(
            name,
            [],
        )

        primary_key = model._meta.pk.name

        for record in records:

            values = dict(record)

            if primary_key not in values:
                raise ValueError(
                    f"Bản ghi {name} thiếu khóa chính " f"'{primary_key}'."
                )

            converted_values = {}

            for field in model._meta.concrete_fields:

                if field.name not in values:
                    continue

                value = values[field.name]

                try:
                    converted_values[field.name] = field.to_python(value)

                except (TypeError, ValueError) as exc:

                    raise ValueError(
                        f"Giá trị trường '{field.name}' "
                        f"của model '{name}' không hợp lệ."
                    ) from exc

            primary_key_value = converted_values.pop(primary_key)

            model.objects.update_or_create(
                **{
                    primary_key: primary_key_value,
                },
                defaults=converted_values,
            )

            count += 1

        restored[name] = count

    return restored


def restore_database(request):
    """
    Restore database từ JSON backup.
    """

    try:
        payload = request.data

        restored = restore_backup(payload)

        return JsonResponse(
            {
                "message": "Restore database thành công.",
                "data": restored,
            },
            status=200,
        )

    except ValueError as e:

        return JsonResponse(
            {
                "error": str(e),
            },
            status=400,
        )

    except Exception as e:

        message, status_code = get_sql_error(e)

        return JsonResponse(
            {
                "error": message,
            },
            status=status_code,
        )
