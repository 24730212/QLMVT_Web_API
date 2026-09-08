def get_sql_error(error):
    message = str(error)

    # SQL Server RAISERROR
    if "50000" in message:
        if "[SQL Server]" in message:
            message = message.split("[SQL Server]", 1)[1]

        if " (50000)" in message:
            message = message.split(" (50000)", 1)[0]

        return message.strip(), 400

    # Các lỗi khác: connection, network, database,...
    return "Lỗi hệ thống hoặc kết nối cơ sở dữ liệu.", 500