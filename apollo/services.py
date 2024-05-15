from datetime import datetime


def print_sensors_data(sensors: dict) -> str:
    """Creates 20x4 string for an LCD screen."""
    index = ["\\", "|", "/", "—"][int(datetime.now().timestamp() % 20 % 4)]
    curr_time = sensors["RCT"]["created_at"].strftime("%H:%M:%S")
    return (
        f"AIR: {sensors['IAM']['temp']:2.1f}  HMD: {sensors['IAM']['humidity']:2.1f}"
        f"RCT: {sensors['RCT']['temp']:2.1f}  CON: {sensors['CON']['temp']:2.1f}"
        f"FLO: {sensors['FLO']['temp']:2.1f}  FUP: {sensors['FUP']['temp']:2.1f}"
        f"STG: {sensors['STG']['temp']:2.1f}  {curr_time}{index}"
    )
