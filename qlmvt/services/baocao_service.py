from django.db import connection


class BaoCaoService:

    @staticmethod
    def get_kpi_nhan_vien():

        with connection.cursor() as cursor:

            cursor.execute("""
                SELECT *
                FROM dbo.fn_BangKPI_NhanVien()
                ORDER BY TongDaXuLy DESC
            """)

            columns = [column[0] for column in cursor.description]

            return [dict(zip(columns, row)) for row in cursor.fetchall()]

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
