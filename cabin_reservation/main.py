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

def print_room_status(system, room_id, current_time):
    """打印某个舱室的当前状态和日程安排"""
    status_info = system.check_status(room_id)
    print(f"\n⏰ 当前时刻: {current_time.isoformat()}")
    print(f"🔧 舱室编号: {room_id}")
    print(f"📌 当前状态: {status_info['status']}")
    
    print("📄 日程安排:")
    formatted_schedule = format_schedule(status_info["schedule"])
    for line in formatted_schedule:
        print(line)
    
    free_slots = [slot for slot in status_info["schedule"] if slot['status'] == '空闲']
    booked_slots = [slot for slot in status_info["schedule"] if slot['status'] == '已预约']
    in_use_slots = [slot for slot in status_info["schedule"] if slot['status'] == '使用中']
    
    print(f"\n🟢 可预约时段: {len(free_slots)} 个")
    print(f"🔵 已预约时段: {len(booked_slots)} 个")
    print(f"🔴 使用中时段: {len(in_use_slots)} 个")
    
    return status_info

def simulate_cabin_reservation():
    print("=== 模拟舱室预约与自动释放场景 ===\n")

    # 初始化系统
    system = ReservationService()
    
    # 添加两个舱室
    room1_id = system.add_room(10)  # 单价10元的舱室
    room2_id = system.add_room(15)  # 单价15元的舱室
    
    now = datetime.now().replace(microsecond=0)

    # 初始状态（当前时间）
    print("---------- 阶段 1：初始状态 ----------")
    print_room_status(system, room1_id, now)
    print_room_status(system, room2_id, now)

    # 阶段1：用户进行预约（+10分钟）
    phase1_time = now + timedelta(minutes=10)
    print("\n\n---------- 阶段 2：用户预约一些时间段 ----------")
    print(f"⏳ 模拟时间前进至: {phase1_time.isoformat()}")
    
    # 房间1预约第一个时间段
    status_info1 = system.check_status(room1_id)
    free_slots1 = [s for s in status_info1["schedule"] if s['status'] == '空闲']
    if free_slots1:
        first_slot = free_slots1[0]
        result = system.make_reservation(room1_id, first_slot['start'], first_slot['end'])
        print(f"\n✅ 舱室 {room1_id} 成功预约时间段: {first_slot['start']} - {first_slot['end']}")
    
    # 房间2预约中间一个时间段
    status_info2 = system.check_status(room2_id)
    free_slots2 = [s for s in status_info2["schedule"] if s['status'] == '空闲']
    if len(free_slots2) > 2:
        selected_slot = free_slots2[2]
        result = system.make_reservation(room2_id, selected_slot['start'], selected_slot['end'])
        print(f"\n✅ 舱室 {room2_id} 成功预约时间段: {selected_slot['start']} - {selected_slot['end']}")
    
    # 打印更新后的状态
    print_room_status(system, room1_id, phase1_time)
    print_room_status(system, room2_id, phase1_time)

    # 阶段2：开始使用（+30分钟）
    phase2_time = now + timedelta(minutes=30)
    print("\n\n---------- 阶段 3：用户开始使用预约的时间段 ----------")
    print(f"⏳ 模拟时间前进至: {phase2_time.isoformat()}")
    
    # 开始使用房间1的预约
    if free_slots1:
        start_time = free_slots1[0]['start']
        end_time = free_slots1[0]['end']
        
        # 修改舱室的 usage_start_time 直接进入使用中状态
        room = system.rooms[room1_id]
        room.status = RoomStatus.IN_USE
        room.usage_start_time = datetime.fromisoformat(start_time)
        
        print(f"🔵 舱室 {room1_id} 开始使用时间段: {start_time} - {end_time}")
    
    # 打印更新后的状态
    print_room_status(system, room1_id, phase2_time)
    print_room_status(system, room2_id, phase2_time)

    # 阶段3：新预约（+60分钟）
    phase3_time = now + timedelta(minutes=60)
    print("\n\n---------- 阶段 4：新的预约请求 ----------")
    print(f"⏳ 模拟时间前进至: {phase3_time.isoformat()}")
    
    # 尝试预约房间2的一个新时间段
    status_info2 = system.check_status(room2_id)
    free_slots2 = [s for s in status_info2["schedule"] if s['status'] == '空闲']
    if free_slots2:
        selected_slot = free_slots2[0]
        result = system.make_reservation(room2_id, selected_slot['start'], selected_slot['end'])
        if result['status'] == 'success':
            print(f"\n✅ 舱室 {room2_id} 成功预约时间段: {selected_slot['start']} - {selected_slot['end']}")
        else:
            print(f"\n❌ 舱室 {room2_id} 预约失败: {result['message']}")
    
    # 打印更新后的状态
    print_room_status(system, room1_id, phase3_time)
    print_room_status(system, room2_id, phase3_time)

    # 阶段4：时间到，自动释放（超过房间1的使用时间）
    released_time = datetime.fromisoformat(free_slots1[0]['end']) + timedelta(seconds=1)
    print(f"\n\n---------- 阶段 5：时间到达，舱室释放 ----------")
    print(f"⏳ 模拟时间前进至: {released_time.isoformat()}")
    
    # 自动释放超时的舱室
    released_rooms = []
    for room_id in [room1_id, room2_id]:
        room = system.rooms[room_id]
        if room.status == RoomStatus.IN_USE and released_time >= (room.usage_start_time + timedelta(hours=1)):
            room.release()
            released_rooms.append(room_id)
    
    # 打印释放情况
    if released_rooms:
        print(f"\n🚪 以下舱室已自动释放: {', '.join(map(str, released_rooms))}")
    else:
        print("\n⚠️ 暂无舱室需要释放")
    
    # 打印最终状态
    print_room_status(system, room1_id, released_time)
    print_room_status(system, room2_id, released_time)

    print("\n✅ 场景模拟完成")

if __name__ == "__main__":
    simulate_cabin_reservation()