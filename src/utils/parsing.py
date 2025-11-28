import re
import string

# Включает следующие типы символов:
# - знаки препинания (string.punctuation): !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
# - перенос строки (\n)
# - возврат каретки (\r)
# - табуляция (\t)
# - перевод формы (\f)
# - вертикальная табуляция (\v)
# - любые пробельные символы (\s)
# - знак плюс (+)
CHARS_TO_CLEAN_REGEX = rf"[{re.escape(string.punctuation)}\n\r\t\f\v\s+]"

SEARCH_CHAR = "%"


def prepare_text_for_search(text: str):
    # Remove trailing spaces
    text = text.strip()
    # Replace special chars
    text = re.sub(CHARS_TO_CLEAN_REGEX, SEARCH_CHAR, text)
    # Add search char at start and end
    text = f"{SEARCH_CHAR}{text}{SEARCH_CHAR}"
    return text
