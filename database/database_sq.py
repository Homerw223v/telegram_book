import sqlite3

base = sqlite3.connect('tg_book.db')
cur = base.cursor()


async def sql_start():
    """Creating database"""
    if base:
        base.execute(
            'CREATE TABLE IF NOT EXISTS readers('
            'user_id INT PRIMARY KEY,'
            'username TEXT,'
            'page SMALLINT);'
        )
        base.execute(
            'CREATE TABLE IF NOT EXISTS bookmarks('
            'id INTEGER PRIMARY KEY AUTOINCREMENT,'
            'user_id INT,'
            'page INT)'
        )
    base.commit()
