from services.reservation_service import ReservationService, RoomStatus
from datetime import datetime, timedelta
import random

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
    print("=== 测试预约查询系统 ===")
    
    # 初始化系统并添加舱室
    system = ReservationService()
    room_id = system.add_room(100)  # 添加一个单价为100元的舱室
    
    # 查询初始的日程安排
    status = system.check_status(room_id)
    assert status is not None, "舱室状态不应为 None"
    
    raw_schedule = status["schedule"]


    initial_total_slots = len(raw_schedule) if raw_schedule else 0
    assert initial_total_slots > 0, "应有时间段信息"
    
    # 验证初始舱室状态为空闲
    assert status["status"] == RoomStatus.FREE.value, "初始状态应为空闲"
    
    # 插入随机预约
    # print("\n--- 插入随机预约阶段 ---")
    # 获取所有空闲时段
    free_slots = [slot for slot in raw_schedule if slot['status'] == '空闲']
    num_slots_to_book = min(random.randint(1, 3), len(free_slots))  # 随机预约1-3个时间段
    
    # print(f"尝试随机预约 {num_slots_to_book} 个时间段")
    successful_bookings = 0
    
    # 随机选择并预约
    if free_slots:
        selected_slots = random.sample(free_slots, num_slots_to_book)
        
        for slot in selected_slots:
            # print(f"\n尝试预约时间段: {slot['start']} - {slot['end']}")
            
            # 执行预约操作
            result = system.make_reservation(room_id, slot['start'], slot['end'])
            # print(f"预约结果: {result['status']} - {result['message']}")
            
            if result['status'] == 'success':
                successful_bookings += 1
    
    # 刷新状态
    updated_status = system.check_status(room_id)
    updated_free_slots = [slot for slot in updated_status["schedule"] if slot['status'] == '空闲']
    
    # 验证空闲时间段减少
    # print(f"\n查询到的舱室安排（经过随机预约）:")
    # updated_formatted_schedule = format_schedule(updated_status["schedule"])
    # for line in updated_formatted_schedule:
    #     print(line)
    
    # 更新自由时隙数量
    updated_free_slots = [slot for slot in updated_status["schedule"] if slot['status'] == '空闲']
    print(f"\n当前剩余空闲时间段数量: {len(updated_free_slots)}")
    
    # 验证预约是否成功
    assert len(updated_free_slots) == len(free_slots) - successful_bookings, \
        f"空闲时间段应减少{successful_bookings}个，实际减少{len(free_slots) - len(updated_free_slots)}"
    
    # 进行一次预约（预约第一个时间段）
    free_slots = [slot for slot in updated_status["schedule"] if slot['status'] == '空闲']
    if free_slots:
        first_slot = free_slots[0]
        # print(f"\n尝试预约时间段: {first_slot['start']} - {first_slot['end']}")
        
        # 执行预约操作
        result = system.make_reservation(room_id, first_slot['start'], first_slot['end'])
        # print(f"预约结果: {result['status']} - {result['message']}")
        assert result['status'] == 'success', "预约应成功"
        
        # 验证舱室状态变为已预约
        final_status = system.check_status(room_id)
        assert final_status["status"] == RoomStatus.BOOKED.value, "预约后状态应为已预约"
        
        # 验证空闲时间段减少
        final_free_slots = [slot for slot in final_status["schedule"] if slot['status'] == '空闲']
        print(f"\n查询到的舱室安排（经过随机预约）:")
        final_formatted_schedule = format_schedule(final_status["schedule"])
        for line in final_formatted_schedule:
            print(line)
            
        assert len(final_free_slots) == len(updated_free_slots) - 1, \
            "空闲时间段应再减少1个"
        
        # 验证已预约时间段增加
        booked_slots = [slot for slot in final_status["schedule"] if slot['status'] == '已预约']
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