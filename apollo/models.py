from datetime import datetime
from decimal import Decimal
from typing import Any

from pydantic import BaseModel


class Sensor(BaseModel):
    id: int | None = None
    created_at: datetime | None = None
    synced_at: datetime | None = None

    sensor_id: str
    temp: Decimal | None = None
    context: dict | None = None

    label_warm: str | None = None
    label_shine: str | None = None

    def __init__(self, /, **data: Any) -> None:
        super().__init__(**data)

    @property
    def label(self):
        return self.label_warm if self.context["mode"] == "warm" else self.label_shine
