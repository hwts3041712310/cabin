from models.cabin import CabinRoom, RoomStatus
from datetime import datetime, timedelta

class ReservationService:
    def __init__(self):
        self.rooms = {}
        self.next_room_id = 1

    def add_room(self, hourly_rate):
        room_id = self.next_room_id
        self.rooms[room_id] = CabinRoom(room_id, hourly_rate)
        self.next_room_id += 1
        return room_id

    def remove_room(self, room_id):
        if room_id in self.rooms:
            del self.rooms[room_id]
            return True
        return False

    def get_room_status(self, room_id):
        if room_id in self.rooms:
            room = self.rooms[room_id]
            return {
                "room_id": room.room_id,
                "status": room.status.value,
                "hourly_rate": room.hourly_rate,
                "available_slots": self.get_available_slots(room_id),
                "booked_slots": self.get_booked_slots(room_id)
            }
        return None
        
    def get_booked_slots(self, room_id):
        """获取舱室已预约的时间段"""
        if room_id in self.rooms:
            return [{
                "start": slot["start"].isoformat(),
                "end": slot["end"].isoformat(),
                "date": slot["start"].date().isoformat()
            } for slot in self.rooms[room_id].booking_slots]
        return []

    def check_status(self, room_id):
        """检查并返回舱室的完整状态信息，包括所有时间段的状态"""
        if room_id not in self.rooms:
            return None
            
        room = self.rooms[room_id]
        now = datetime.now()
        schedule = []
        
        # 生成未来3天的所有时间段（6:00-10:00）
        for day in range(3):
            base_date = now.replace(hour=6, minute=0, second=0, microsecond=0) + timedelta(days=day)
            
            for hour in range(6, 10):
                start_time = base_date.replace(hour=hour, minute=0)
                end_time = base_date.replace(hour=hour+1, minute=0)
                
                # 判断时间段状态
                status = "空闲"
                for slot in room.booking_slots:
                    if not (end_time <= slot["start"] or start_time >= slot["end"]):
                        if room.status == RoomStatus.IN_USE and \
                           start_time <= now <= end_time:
                            status = "使用中"
                        else:
                            status = "已预约"
                        break
                        
                schedule.append({
                    "start": start_time.isoformat(),
                    "end": end_time.isoformat(),
                    "date": start_time.date().isoformat(),
                    "status": status,
                    "status_display": dict(RoomStatus.__members__).get(status).value if status in dict(RoomStatus.__members__) else status
                })
                    
        return {
            "room_id": room.room_id,
            "status": room.status.value,
            "hourly_rate": room.hourly_rate,
            "schedule": schedule
        }

    def get_available_slots(self, room_id, days_ahead=3):
        """获取舱室的可预约时间段"""
        if room_id not in self.rooms:
            return []
        
        now = datetime.now()
        available_slots = []
        
        for day in range(days_ahead):
            base_date = now.replace(hour=6, minute=0, second=0, microsecond=0) + timedelta(days=day)
            
            for hour in range(6, 10):
                start_time = base_date.replace(hour=hour, minute=0)
                end_time = base_date.replace(hour=hour+1, minute=0)
                
                if self.rooms[room_id].check_availability(start_time, end_time):
                    available_slots.append({
                        "start": start_time.isoformat(),
                        "end": end_time.isoformat(),
                        "date": start_time.date().isoformat()
                    })
                    
        return available_slots

    def make_reservation(self, room_id, start_time, end_time):
        if room_id in self.rooms:
            start = datetime.fromisoformat(start_time)
            end = datetime.fromisoformat(end_time)
            
            if self.rooms[room_id].book(start, end):
                return {"status": "success", "message": "预约成功"}
            else:
                return {"status": "error", "message": "时段不可用或舱室已被预订"}
        return {"status": "error", "message": "舱室不存在"}

    def start_reservation(self, room_id):
        if room_id in self.rooms:
            if self.rooms[room_id].start_use():
                return {"status": "success", "message": "开始使用"}
            else:
                return {"status": "error", "message": "无法开始使用，舱室不在可使用状态"}
        return {"status": "error", "message": "舱室不存在"}

    def end_reservation(self, room_id):
        if room_id in self.rooms:
            room = self.rooms[room_id]
            duration = 0
            
            if room.status == RoomStatus.IN_USE:
                duration = (datetime.now() - room.usage_start_time).total_seconds() / 60
            elif room.status == RoomStatus.BOOKED:
                duration = (datetime.now() - room.booking_slots[-1]["start"]).total_seconds() / 60
                
            cost = room.calculate_cost(duration)
            
            if room.release():
                return {"status": "success", "message": "舱室已释放", "cost": round(cost, 2)}
            else:
                return {"status": "error", "message": "无法释放舱室"}
        return {"status": "error", "message": "舱室不存在"}

    def update_room_info(self, room_id, hourly_rate=None):
        if room_id in self.rooms:
            room = self.rooms[room_id]
            if hourly_rate:
                room.hourly_rate = hourly_rate
            return {"status": "success", "message": "信息更新成功"}
        return {"status": "error", "message": "舱室不存在"}