# Хорошая практика: асинхронный цикл
async def get_users(conn, query):
    """Пример хорошего кода"""
    async for row in conn.execute(query):
        process_row(row)

async def get_first(conn, query):
    """fetchone() разрешен, так как нам нужна только одна строка"""
    row = await conn.execute(query).fetchone()
    return row
