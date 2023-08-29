from .database_sq import cur, base


async def get_user(user_id: int) -> tuple:
    """Function for getting user from database
    :param user_id: An integer, user id in telegram
    :type user_id: int

    :rtype: tuple
    :return Information about user
    """
    return cur.execute('SELECT * FROM readers WHERE user_id = ?', (user_id,)).fetchone()


async def create_reader(user_id: int, username: str) -> None:
    """Function for creating reader
    :param user_id: An integer, user id in telegram
    :type user_id: int
    :param username: A username from telegram
    :type username: str

    :rtype: None
    """
    cur.execute('INSERT INTO readers(user_id, username, page) VALUES (?,?,?)', (user_id, username, 1,))
    base.commit()


async def set_page(user_id: int, page: int = 1) -> int | None:
    """Function for set current page
    :param user_id: An integer, user id in telegram
    :type user_id: int
    :param page: An integer, number of page
    :type page: int
    :raise AttributionError: If user does not exist in database

    :rtype: [int, None]
    :return: Number of saved page
    """
    try:
        cur.execute('UPDATE readers SET page=? WHERE user_id=?', (page, user_id))
        base.commit()
        return page
    except AttributeError:
        return None


async def get_page(user_id: int) -> int | None:
    """Function for getting current page
    :param user_id: An integer, user id in telegram
    :type user_id: int

    :rtype: [int, None]
    :return: Page from which to continue reading
    """
    page = cur.execute('SELECT page FROM readers WHERE user_id=?', (user_id,)).fetchone()[0]
    return page


async def get_user_bookmarks(user_id: int) -> list | None:
    """Function for getting all bookmarks for user
    :param user_id: An integer, user id in telegram
    :type user_id: int
    :raise IndexError: If there are no bookmarks in database

    :rtype: list | None
    :return: All bookmarks for user
    """
    answer = cur.execute('SELECT page FROM bookmarks WHERE user_id=?', (user_id,)).fetchall()
    try:
        bookmarks = [i[0] for i in answer]
        bookmarks.sort()
        return bookmarks
    except IndexError:
        return None


async def add_bookmark(user_id: int, page: int) -> None:
    """
    Function to add a new bookmark
    :param user_id: An integer, user id in telegram
    :type user_id: int
    :param page: An integer, number of page
    :type page: int

    :rtype: None
    """
    exists = cur.execute('SELECT * FROM bookmarks WHERE user_id=? AND page=?', (user_id, page,)).fetchone()
    if not exists:
        cur.execute('INSERT INTO bookmarks(user_id, page) VALUES(?,?)', (user_id, page,))
        base.commit()


async def delete_bookmark(user_id: int, page: int) -> None:
    """
    Function to delete a bookmark
    :param user_id: An integer, user id in telegram
    :type user_id: int
    :param page: An integer, number of page
    :type page: int

    :rtype: None
    """
    cur.execute('DELETE FROM bookmarks WHERE user_id=? AND page=?', (user_id, page))
    base.commit()
