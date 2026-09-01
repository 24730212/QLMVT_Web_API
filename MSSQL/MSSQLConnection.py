import pyodbc
import os
import re
from pathlib import Path
from django.conf import settings

class SQLConnection:
    def __init__(self):
        self.SERVER = f"{settings.DB_HOST},{settings.DB_PORT}"
        self.DATABASE = settings.DB_NAME
        self.USERNAME = settings.DB_USER
        self.PASSWORD = settings.DB_PASSWORD
        self.SQL_FOLDER = Path(settings.BASE_DIR) / "database" / "sql_thuc_thi"

        self.files = [
            # Roles
            "AdminRole.sql",
            "TechRole.sql",
            # Functions
            "fn_BangKPI_NhanVien.sql",
            "fn_LoHongDaXuLy.sql",
            "fn_SuCoDaXuLy.sql",
            # Stored Procedures
            "sp_AddDevice.sql",
            "sp_Cursors.sql",
            "sp_DeleteDevice.sql",
            "sp_GetAvailability.sql",
            "sp_GetCapacityPlanning.sql",
            "sp_GetDevices.sql",
            "sp_GetEmployeeKPI.sql",
            "sp_GetEmployees.sql",
            "sp_GetErrorBySeverity.sql",
            "sp_GetErrorLog.sql",
            "sp_GetErrorTrend.sql",
            "sp_GetLinks.sql",
            "sp_GetPerformance.sql",
            "sp_GetStatusSummary.sql",
            "sp_GetTopEmployees.sql",
            "sp_GetVulnerabilities.sql",
            "sp_GetVulnerabilityMap.sql",
            "sp_GetVulnStatus.sql",
            "sp_ImportLoHong_Json.sql",
            "sp_ImportNhatKyLoi_Json.sql",
            "sp_Login.sql",
            # Triggers
            "trg_AutoIncident_FromPerformance.sql",
            "trg_BlockDeleteAdminEmployee.sql",
            "trg_BlockDeleteDevice.sql",
            "trg_BlockDeleteErrorLog_WhenUnresolved.sql",
            "trg_BlockDeleteLink_WhenDeviceOn.sql",
            "trg_BlockDeleteVulnerability_Unresolved.sql",
            "trg_IncidentHandlingSLA.sql",
            "trg_LimitEmployeeIncident_Assignments.sql",
            "trg_LimitEmployeeVulnerability_Cases.sql",
            "trg_ValidateDeviceTypeByName.sql",
            "trg_ValidateVulnerabilityTimes.sql",
        ]

        self.conn = None
        self.cursor = None

    # =========================
    # Kết nối database
    # =========================
    def connect(self):
        try:
            connection_string = (
                "DRIVER={ODBC Driver 18 for SQL Server};"
                f"SERVER={self.SERVER};"
                f"DATABASE={self.DATABASE};"
                f"UID={self.USERNAME};"
                f"PWD={self.PASSWORD};"
                "TrustServerCertificate=yes;"
            )

            self.conn = pyodbc.connect(connection_string)
            self.cursor = self.conn.cursor()

            print(f"Đã kết nối database: {self.DATABASE}")
            print("=" * 60)
        except Exception as e:
            print("Test: Error in connection: ", e)

    # =========================
    # Đọc file SQL
    # =========================
    def read_sql_file(self, filepath):
        with open(filepath, "rb") as f:
            raw = f.read()

        if raw.startswith(b"\xff\xfe") or raw.startswith(b"\xfe\xff"):
            return raw.decode("utf-16")

        return raw.decode("utf-8-sig")

    # =========================
    # Tách SQL theo GO
    # =========================
    def split_batches(self, sql):
        return re.split(r"(?im)^\s*GO\s*(?:--.*)?$", sql)

    # =========================
    # Chạy một file SQL
    # =========================
    def execute_file(self, filename):
        filepath = os.path.join(self.SQL_FOLDER, filename)

        print(f"\n>>> Đang chạy: {filename}")

        if not os.path.exists(filepath):
            print(f"!!! Không tìm thấy file: {filepath}")
            return False

        try:
            sql = self.read_sql_file(filepath)
            batches = self.split_batches(sql)

            for batch in batches:
                batch = batch.strip()

                if batch:
                    self.cursor.execute(batch)

            self.conn.commit()

            print(f"✓ Thành công: {filename}")
            return True

        except Exception as e:
            self.conn.rollback()

            print(f"✗ LỖI: {filename}")
            print(e)

            return False

    # =========================
    # Chạy toàn bộ file
    # =========================
    def run(self):
        try:
            self.connect()

            for filename in self.files:
                success = self.execute_file(filename)

                if not success:
                    print("\n!!! Dừng chương trình do có lỗi.")
                    break

        except Exception as e:
            print("\n✗ Không thể kết nối database.")
            print(e)

        finally:
            self.close()

        print("\n" + "=" * 60)
        print("Hoàn tất.")

    # =========================
    # Đóng kết nối
    # =========================
    def close(self):
        if self.cursor:
            self.cursor.close()

        if self.conn:
            self.conn.close()


# ==========================================
# Chạy chương trình
# ==========================================
if __name__ == "__main__":
    runner = SQLConnection()
    runner.run()
