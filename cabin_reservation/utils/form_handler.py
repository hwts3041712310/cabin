def handle_form_submission(reservation_system, form_data):
    action = form_data.get("action")
    
    if action == "add_room":
        hourly_rate = float(form_data.get("hourly_rate"))
        room_id = reservation_system.add_room(hourly_rate)
        return f"新增舱室成功，编号：{room_id}"
    
    elif action == "remove_room":
        room_id = int(form_data.get("room_id"))
        if reservation_system.remove_room(room_id):
            return f"删除舱室成功（编号：{room_id}）"
        else:
            return f"删除失败，舱室不存在（编号：{room_id})"
    
    elif action == "check_status":
        room_id = int(form_data.get("room_id"))
        status = reservation_system.get_room_status(room_id)
        if status:
            return f"舱室状态信息：{status}"
        else:
            return f"查询失败，舱室不存在（编号：{room_id})"
    
    elif action == "book_room":
        room_id = int(form_data.get("room_id"))
        start_time = form_data.get("start_time")
        end_time = form_data.get("end_time")
        result = reservation_system.make_reservation(room_id, start_time, end_time)
        return f"预约结果：{result['status']} - {result['message']}"
    
    elif action == "start_use":
        room_id = int(form_data.get("room_id"))
        result = reservation_system.start_reservation(room_id)
        return f"开始使用结果：{result['status']} - {result['message']}"
    
    elif action == "end_use":
        room_id = int(form_data.get("room_id"))
        result = reservation_system.end_reservation(room_id)
        return f"{result['status']} - {result['message']}，费用：{result.get('cost', 0):.2f}元"
    
    elif action == "update_info":
        room_id = int(form_data.get("room_id"))
        hourly_rate = float(form_data.get("hourly_rate"))
        result = reservation_system.update_room_info(room_id, hourly_rate)
        return f"更新结果：{result['status']} - {result['message']}"
    
    else:
        return "未知操作"