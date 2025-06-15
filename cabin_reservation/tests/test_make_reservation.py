from services.reservation_service import ReservationService
from datetime import datetime, timedelta

def test_make_reservation():
    print("=== 测试确定预约并检查更新后的可预约时间 ===")
    
    # 初始化系统并添加舱室
    system = ReservationService()
    room_id = system.add_room(100)  # 添加一个单价为100元的舱室
    
    # 查询初始的可预约时间段
    status_before = system.get_room_status(room_id)
    available_slots_before = status_before['available_slots']
    print(f"预约前可预约时间段: {available_slots_before}")
    
    # 选择第一个时间段进行预约
    if available_slots_before:
        first_slot = available_slots_before[0]
        start_time = first_slot['start']
        end_time = first_slot['end']
        
        # 执行预约操作
        result = system.make_reservation(room_id, start_time, end_time)
        print(f"预约结果: {result}")
        assert result['status'] == 'success', "预约应成功"
        
        # 查询预约后的状态
        status_after = system.get_room_status(room_id)
        available_slots_after = status_after['available_slots']
        print(f"预约后可预约时间段: {available_slots_after}")
        
        # 验证预约后该时间段不应再出现在可预约列表中
        slot_still_available = any(slot['start'] == start_time and slot['end'] == end_time 
                                 for slot in available_slots_after)
        assert not slot_still_available, "预约后该时间段不应再出现在可预约列表中"
        
        print("✅ 确定预约并检查更新后的可预约时间测试通过")
    else:
        print("没有可预约时间段，无法进行预约测试")

if __name__ == "__main__":
    test_make_reservation()