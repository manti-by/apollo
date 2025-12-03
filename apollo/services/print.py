from __future__ import annotations

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from models import Sensor


def print_sensors_data(sensors: list[Sensor]) -> str:
    """Creates 20x4 string for an LCD screen."""
    sensors: dict[str, Sensor] = {x.sensor_id: x for x in sensors}
    curr_time = sensors["T1"].created_at.strftime("%H:%M:%S")
    return (
        f"RCT: {sensors['T2'].temp:2.1f}  CON: {sensors['T1'].temp:2.1f}"
        f"FLO: {sensors['T3'].temp:2.1f}  FHI: {sensors['T4'].temp:2.1f}"
        f"STG: {sensors['T5'].temp:2.1f}           "
        f"{curr_time}"
    )
