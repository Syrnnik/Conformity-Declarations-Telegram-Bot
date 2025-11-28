DECLARATION_URL = (
    "https://pub.fsa.gov.ru/rds/declaration/view/{declaration_id}/declaration"
)


def get_declaration_url(declaration_id: int | str):
    url = DECLARATION_URL.format(declaration_id=declaration_id)
    return url
