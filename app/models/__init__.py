from sqlalchemy import ForeignKey, text
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    declared_attr,
    relationship,
)
from sqlalchemy.dialects.postgresql import UUID, TIME, JSONB
from sqlalchemy.types import TIMESTAMP, Boolean, String
from datetime import datetime, time
import re


def camel_to_snake(name):
    return re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()
