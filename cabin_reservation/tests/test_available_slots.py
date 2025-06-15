from services.reservation_service import ReservationService
from datetime import datetime, timedelta

def test_available_slots():
    print("=== 测试查询可预约和已被预定时间段 ===")
    
    # 初始化系统并添加舱室
    system = ReservationService()
    room_id = system.add_room(100)  # 添加一个单价为100元的舱室
    
    # 查询初始的可预约时间段
    status = system.get_room_status(room_id)
    print(f"初始可预约时间段: {status['available_slots']}")
    initial_slots = len(status['available_slots'])
    assert initial_slots > 0, "初始应有可预约时间段"
    
    # 进行一次预约
    now = datetime.now()
    next_hour = now + timedelta(hours=1)
    system.make_reservation(room_id, now.isoformat(), next_hour.isoformat())
    
    # 再次查询可预约时间段，应减少
    status_after_booking = system.get_room_status(room_id)
    print(f"预约后可预约时间段: {status_after_booking['available_slots']}")
    slots_after_booking = len(status_after_booking['available_slots'])
    assert slots_after_booking == initial_slots - 1, "预约后可预约时间段应减少1个"
    
    print("✅ 查询可预约和已被预定时间段测试通过")

if __name__ == "__main__":
    test_available_slots()