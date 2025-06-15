from services.reservation_service import ReservationService
from datetime import datetime, timedelta
from models.cabin import CabinRoom, RoomStatus

def test_check_room_status():
    print("=== 测试查询舱室状态 ===")
    
    # 初始化系统并添加测试舱室
    system = ReservationService()
    room_id = system.add_room(100)  # 添加一个单价为100元的舱室
    
    # 初始状态应为空闲
    status = system.get_room_status(room_id)
    print(f"初始状态: {status}")
    assert status["status"] == RoomStatus.FREE.value, "初始状态应为空闲"
    
    # 预约舱室
    now = datetime.now()
    next_hour = now + timedelta(hours=1)
    system.make_reservation(room_id, now.isoformat(), next_hour.isoformat())
    
    # 预约后状态应为已预约
    status = system.get_room_status(room_id)
    print(f"预约后状态: {status}")
    assert status["status"] == RoomStatus.BOOKED.value, "预约后状态应为已预约"
    
    print("✅ 查询舱室状态测试通过")

if __name__ == "__main__":
    test_check_room_status()