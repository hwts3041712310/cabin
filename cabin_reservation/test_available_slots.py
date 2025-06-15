from services.reservation_service import ReservationService, RoomStatus
from datetime import datetime, timedelta

def format_schedule(schedule):
    """将日程安排格式化为按日期分组的字符串列表"""
    schedule_by_date = {}
    for entry in schedule:
        date_key = entry['date']
        if date_key not in schedule_by_date:
            schedule_by_date[date_key] = []
        schedule_by_date[date_key].append(f"{entry['start']} - {entry['end']} | 状态: {entry['status_display']}")
    
    result = []
    for date, date_entries in sorted(schedule_by_date.items()):
        result.append(f"📅 {date}:")
        for entry in date_entries:
            # 根据不同状态添加颜色标记
            if "空闲" in entry:
                result.append(f"  - 🟢 {entry}")
            elif "已预约" in entry:
                result.append(f"  - 🔵 {entry}")
            elif "使用中" in entry:
                result.append(f"  - 🔴 {entry}")
    
    return result

def test_room_operations():
    print("=== 测试舱室预约系统 ===")
    
    # 初始化系统并添加舱室
    system = ReservationService()
    room_id = system.add_room(100)  # 添加一个单价为100元的舱室
    
    # 查询初始的日程安排
    status = system.check_status(room_id)
    assert status is not None, "舱室状态不应为 None"
    
    raw_schedule = status["schedule"]
    print("\n初始日程安排:")
    formatted_schedule = format_schedule(raw_schedule)
    for line in formatted_schedule:
        print(line)
    
    initial_total_slots = len(raw_schedule) if raw_schedule else 0
    assert initial_total_slots > 0, "应有时间段信息"
    
    # 验证初始舱室状态为空闲
    assert status["status"] == RoomStatus.FREE.value, "初始状态应为空闲"
    
    # 进行一次预约（预约第一个时间段）
    free_slots = [slot for slot in raw_schedule if slot['status'] == '空闲']
    if free_slots:
        first_slot = free_slots[0]
        print(f"\n尝试预约时间段: {first_slot['start']} - {first_slot['end']}")
        
        # 执行预约操作
        result = system.make_reservation(room_id, first_slot['start'], first_slot['end'])
        print(f"预约结果: {result['status']} - {result['message']}")
        assert result['status'] == 'success', "预约应成功"
        
        # 验证舱室状态变为已预约
        updated_status = system.check_status(room_id)
        assert updated_status["status"] == RoomStatus.BOOKED.value, "预约后状态应为已预约"
        
        # 验证空闲时间段减少
        updated_free_slots = [slot for slot in updated_status["schedule"] if slot['status'] == '空闲']
        print("\n更新后日程安排:")
        updated_formatted_schedule = format_schedule(updated_status["schedule"])
        for line in updated_formatted_schedule:
            print(line)
            
        assert len(updated_free_slots) == len(free_slots) - 1, \
            "空闲时间段应减少1个"
        
        # 验证已预约时间段增加
        booked_slots = [slot for slot in updated_status["schedule"] if slot['status'] == '已预约']
        print("\n已预约时间段:")
        if booked_slots:
            for slot in booked_slots:
                print(f"  - {slot['start']} - {slot['end']}")
            assert len(booked_slots) > 0, "应有已预约时间段"
        else:
            print("  - 暂无已预约时间段")
    
    print("\n✅ 舱室预约系统测试通过")

if __name__ == "__main__":
    test_room_operations()