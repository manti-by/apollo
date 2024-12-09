from apollo.conf import MODE


def print_sensors_data(sensors: list) -> str:
    """Creates 20x4 string for an LCD screen."""
    sensors = {x["sensor_id"]: x for x in sensors}
    if MODE == "network":
        return (
            f"CX1: {sensors['CENTAX-1']['temp']:2.1f}*C {sensors['CENTAX-1']['humidity']:2.1f}%"
            f"CX2: {sensors['CENTAX-2']['temp']:2.1f}*C {sensors['CENTAX-2']['humidity']:2.1f}%"
            f"CX3: {sensors['CENTAX-3']['temp']:2.1f}*C {sensors['CENTAX-3']['humidity']:2.1f}%"
            f"CX4: {sensors['CENTAX-4']['temp']:2.1f}*C {sensors['CENTAX-4']['humidity']:2.1f}%"
        )

    curr_time = sensors["REACTOR"]["created_at"].strftime("%H:%M:%S")
    return (
        f"AIR: {sensors['CORUSCANT']['temp']:2.1f}  HMD: {sensors['CORUSCANT']['humidity']:2.1f}"
        f"RCT: {sensors['REACTOR']['temp']:2.1f}  CON: {sensors['CONNECT']['temp']:2.1f}"
        f"FLO: {sensors['FRZR-LO']['temp']:2.1f}  FHI: {sensors['FRZR-HI']['temp']:2.1f}"
        f"STG: {sensors['STORAGE']['temp']:2.1f} {curr_time}"
    )
