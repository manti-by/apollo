from datetime import datetime


def print_sensors_data(sensors: dict) -> str:
    """Creates 20x4 string for an LCD screen."""
    index = ["\\", "|", "/", "—"][int(datetime.now().timestamp() % 20 % 4)]
    curr_time = sensors["REACTOR"]["created_at"].strftime("%H:%M:%S")
    return (
        f"RCT: {sensors['REACTOR']['temp']}  "
        f"CON: {sensors['CONNECT']['temp']}\n"
        f"FLO: {sensors['FRZR-LO']['temp']}  "
        f"FUP: {sensors['FRZR-HI']['temp']}\n"
        f"STG: {sensors['STORAGE']['temp']}\n"
        f"{index}           {curr_time}"
    )
