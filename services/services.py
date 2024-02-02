import asyncio
import os

BOOK_PATH = r'/book/book.txt'
PAGE_SIZE = 800


def _get_part_text(text: str, start: int, size: int) -> tuple[str, int]:
    """Helper function to correct split text
    :rtype: tuple
    :return: A tuple with split text and index of last symbol
    """
    answer: str = text[start : start + size]
    indexes: list = []
    for i in (',', '.', '!', ':', ';', '?'):
        indexes.append(answer.rfind(f'{i}'))
    indexes.sort()
    index: int = max(indexes)
    return answer[: index + 1], index + 1


async def prepare_book(path: str | None):
    """Function for creating a book
    :param path: String path to a book, default None
    :type path: str | None

    :rtype: dict
    :return: A dictionary where key is a number of page and value is a text with max length 800
    """
    text: str = ''
    with open(f'{path}', 'r', encoding='utf-8') as file:
        for line in file.readlines():
            text += line
    start: int = 0
    dictionary: dict[int, str] = dict()
    for page in range(1, 10000):
        func = _get_part_text(text[start:], start=0, size=PAGE_SIZE)
        if func[0]:
            dictionary[page] = func[0].lstrip()
            start += func[1]
        else:
            break
    return dictionary


book: dict = asyncio.run(prepare_book(os.getcwd() + BOOK_PATH))
