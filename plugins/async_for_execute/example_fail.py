# Плохо: использование fetchall() для выгрузки всех строк сразу
async def get_all_users(conn, query):
    """Использование fetchall"""
    rows = (await conn.execute(query)).fetchall()
    
    # Снова плохо
    result = await conn.execute(query)
    data = result.fetchmany(10)
