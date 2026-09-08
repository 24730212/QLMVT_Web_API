from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):

    response = exception_handler(exc, context)

    # DRF không xử lý được exception này
    if response is None:
        return response

    # =====================================================
    # 401 - AUTHENTICATION / JWT
    # =====================================================

    if response.status_code == 401:

        code = response.data.get("code")
        detail = str(response.data.get("detail", "")).lower()

        # -------------------------------------------------
        # JWT không hợp lệ
        # -------------------------------------------------

        if code == "token_not_valid":

            messages = response.data.get("messages", [])

            # Kiểm tra nguyên nhân cụ thể
            for message in messages:

                error_message = str(message.get("message", "")).lower()

                # Access token đã hết hạn
                if "expired" in error_message:

                    response.data = {"error": "Access token đã hết hạn."}

                    return response

                # Sai loại token
                if "wrong type" in error_message:

                    response.data = {"error": "Sai loại token."}

                    return response

            # Token sai chữ ký / token bị hỏng /
            # token không hợp lệ
            response.data = {"error": "Access token không hợp lệ."}

            return response

        # -------------------------------------------------
        # Chưa đăng nhập
        # -------------------------------------------------

        if "authentication credentials were not provided" in detail:

            response.data = {"error": "Bạn chưa đăng nhập."}

            return response

        # -------------------------------------------------
        # Các lỗi authentication khác
        # -------------------------------------------------

        response.data = {"error": response.data.get("detail", "Xác thực thất bại.")}

        return response

    # =====================================================
    # 403 - KHÔNG CÓ QUYỀN
    # =====================================================

    if response.status_code == 403:

        response.data = {"error": "Bạn không có quyền thực hiện thao tác này."}

        return response

    # =====================================================
    # CÁC LỖI KHÁC
    # =====================================================

    return response
