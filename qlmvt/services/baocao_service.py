from django.db import connection


class BaoCaoService:

    @staticmethod
    def get_kpi_nhan_vien(ma_nv=None):

        with connection.cursor() as cursor:

            cursor.execute("""
                SELECT *
                FROM dbo.fn_BangKPI_NhanVien()
                ORDER BY TongDaXuLy DESC
            """)

            columns = [column[0] for column in cursor.description]

            data = [dict(zip(columns, row)) for row in cursor.fetchall()]

            # User chỉ được xem KPI của chính mình
            if ma_nv is not None:
                data = [item for item in data if item["MaNV"] == ma_nv]

            return data

    @staticmethod
    def get_lo_hong_theo_thiet_bi():
        with connection.cursor() as cursor:
            cursor.execute("EXEC dbo.sp_GetVulnerabilityMap")

            rows = cursor.fetchall()

            return [
                {
                    "ten_tb": row[0],
                    "tong_lo_hong": (row[1] + row[2] + row[3] + row[4]),
                    "muc_do": {
                        "critical": row[1],
                        "high": row[2],
                        "medium": row[3],
                        "low": row[4],
                    },
                }
                for row in rows
            ]
