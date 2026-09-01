-- 1. Quản lý cấu hình thiết bị và sơ đồ liên kết
GRANT SELECT, INSERT, UPDATE, DELETE ON ThietBi TO TechRole;
GRANT SELECT, INSERT, UPDATE, DELETE ON LienKet TO TechRole;

-- 2. Theo dõi và quản lý vận hành
GRANT SELECT, INSERT, UPDATE, DELETE ON ChiSoHieuSuat TO TechRole;
GRANT SELECT, INSERT, UPDATE, DELETE ON NhatKyLoi TO TechRole;

-- 3. Quản lý thông tin nhân sự
GRANT SELECT ON NhanVien TO TechRole; 
DENY INSERT, UPDATE, DELETE ON NhanVien TO TechRole; 
GO