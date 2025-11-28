from aiohttp import ClientSession

from constants.declarationsStatuses import DeclarationStatus
from utils.api.auth import get_auth_token
from utils.parsing import prepare_text_for_search

DECLARATIONS_API_URL = "https://pub.fsa.gov.ru/api/v1/rds/common/declarations/get"


def build_search_body(
    manufacturer: str,
    product: str,
):
    product = prepare_text_for_search(product)
    manufacturer = prepare_text_for_search(manufacturer)

    columns_search = []

    # Manufacturer
    if manufacturer:
        columns_search.append(
            {
                "name": "manufacterName",
                "search": manufacturer,
            }
        )

    # Product
    columns_search.append(
        {
            "name": "productFullName",
            "search": product,
        }
    )

    body = {
        "size": 100,
        "page": 0,
        "filter": {
            "status": [
                DeclarationStatus.ACTUAL,
            ],
            "columnsSearch": columns_search,
        },
        "columnsSort": [
            {
                "column": "declDate",
                "sort": "DESC",
            },
        ],
    }
    return body


async def get_declarations(
    manufacturer: str,
    product: str,
) -> list[dict]:
    """
    Отправляет POST запрос на DECLARATIONS_API_URL с составленным body для поиска деклараций.
    """

    # Get Auth Token
    token = await get_auth_token()
    headers = {
        "Authorization": f"Bearer {token}",
    }

    # Get Declarations by filters
    body = build_search_body(manufacturer, product)
    async with ClientSession() as session:
        response = await session.post(
            url=DECLARATIONS_API_URL,
            json=body,
            headers=headers,
        )
        response.raise_for_status()

        response_data: dict = await response.json()
        declarations: list[dict] = response_data.get("items", [])

        return declarations
