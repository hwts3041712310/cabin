from services.reservation_service import ReservationService
from datetime import datetime, timedelta

def test_check_price():
    print("=== 测试查询舱室价格信息 ===")
    
    # 初始化系统并添加不同价格的舱室
    system = ReservationService()
    room1_id = system.add_room(15)  # 单价15元的舱室
    room2_id = system.add_room(20)  # 单价20元的舱室
    
    # 查询舱室1的价格
    status1 = system.get_room_status(room1_id)
    print(f"舱室 {room1_id} 的价格: {status1['hourly_rate']} 元/小时")
    assert status1["hourly_rate"] == 15, "舱室1的价格应为10元/小时"
    
    # 查询舱室2的价格
    status2 = system.get_room_status(room2_id)
    print(f"舱室 {room2_id} 的价格: {status2['hourly_rate']} 元/小时")
    assert status2["hourly_rate"] == 20, "舱室2的价格应为15元/小时"
    
    print("✅ 查询价格信息测试通过")

if __name__ == "__main__":
    test_check_price()