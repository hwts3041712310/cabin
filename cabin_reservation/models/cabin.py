from datetime import datetime, timedelta
from enum import Enum

class RoomStatus(Enum):
    FREE = "空闲"
    BOOKED = "已预约"
    IN_USE = "使用中"

class CabinRoom:
    def __init__(self, room_id, hourly_rate):
        self.room_id = room_id
        self.status = RoomStatus.FREE
        self.hourly_rate = hourly_rate
        self.booking_slots = []
        self.usage_start_time = None

    def book(self, start_time, end_time):
        if self.check_availability(start_time, end_time):
            self.booking_slots.append({"start": start_time, "end": end_time})
            self.status = RoomStatus.BOOKED
            return True
        return False

    def start_use(self):
        if self.status == RoomStatus.BOOKED:
            self.status = RoomStatus.IN_USE
            self.usage_start_time = datetime.now()
            return True
        return False

    def release(self):
        if self.status in [RoomStatus.IN_USE, RoomStatus.BOOKED]:
            self.status = RoomStatus.FREE
            self.booking_slots = [slot for slot in self.booking_slots 
                                 if not (slot['start'] <= datetime.now() <= slot['end'])]
            self.usage_start_time = None
            return True
        return False

    def check_availability(self, start_time, end_time):
        for slot in self.booking_slots:
            if not (end_time <= slot["start"] or start_time >= slot["end"]):
                return False
        return True

    def calculate_cost(self, duration_minutes):
        return (duration_minutes / 15) * (self.hourly_rate / 4)