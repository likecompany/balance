from sqlalchemy import types
from sqlalchemy.orm import mapped_column
from typing_extensions import Annotated

BigInt = Annotated[int, mapped_column(types.BIGINT)]
