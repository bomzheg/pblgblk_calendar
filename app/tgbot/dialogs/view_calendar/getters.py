from datetime import date
from typing import Any


async def get_forbidden(**_) -> dict[str, Any]:
    return {
        "forbidden": [
            date(2025, 12, 18),
            date(2025, 12, 28),
        ]
    }