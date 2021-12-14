from dataclasses import dataclass


@dataclass(frozen=False)
class Config:

    window_time_ahead_in_days: int = 14
    """The days ahead to check for making appointments"""

    doctor_work_start_hour: int = 8

    doctor_work_end_hour: int = 17

    min_ahead_showing_availability: int = 60 * 24 * 1

    time_unit: int = 30
    """Time unit in minute."""