from fastapi.responses import StreamingResponse
from fastapi import APIRouter, HTTPException

router = APIRouter()


def get_displayed_value(number: int, int1: int, int2: int, str1: str, str2: str) -> str:
    entry = ""
    if number % int1 == 0:
        entry += str1
    if number % int2 == 0:
        entry += str2
    elif not entry:
        entry += str(number)
    return entry


def generate_response(int1: int, int2: int, str1: str, str2: str, limit: int):

    yield get_displayed_value(
        number=1,
        int1=int1,
        int2=int2,
        str1=str1,
        str2=str2
    )

    for i in range(2, limit + 1):
        entry = get_displayed_value(
            number=i,
            int1=int1,
            int2=int2,
            str1=str1,
            str2=str2
        )
        yield f", {entry}"


@router.get("/fizz-buzz")
async def fizz_buzz(int1: int, int2: int, str1: str, str2: str, limit: int = 100) -> StreamingResponse:
    if limit < 1:
        raise HTTPException(
            status_code=400,
            detail="Limit must be a positive integer greater or equal to 1",
        )
    if int1 < 1 or int2 < 1:
        raise HTTPException(
            status_code=400,
            detail="int1 and int2 must be positive integers greater or equal to 1",
        )
    return StreamingResponse(
        generate_response(
            int1=int1,
            int2=int2,
            str1=str1,
            str2=str2,
            limit=limit
        ),
        media_type="text/plain",
    )
