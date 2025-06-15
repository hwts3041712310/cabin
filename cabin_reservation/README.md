# 舱室预约管理系统

这是一个基础的舱室预约管理系统后端实现，使用 Python 编写，包含基本的舱室状态管理、预约、计费和自动释放功能。

## 功能特性

- 舱室编号管理
- 状态跟踪（空闲、已预约、使用中）
- 可预约时段管理
- 15分钟为单位的单价计算
- 使用后自动释放
- 表单提交处理及状态反馈

## 文件结构
```
cabin_reservation/
│
├── models/                  # 存放数据模型相关代码
│   ├── __init__.py
│   ├── cabin.py             # 舱室模型定义
│   └── time_slot.py         # 时间段模型定义
│
├── services/                # 存放业务逻辑代码
│   ├── __init__.py
│   └── reservation_service.py  # 预约系统核心服务
│
├── utils/                   # 存放工具类代码
│   ├── __init__.py
│   └── form_handler.py      # 表单处理工具
│
├── tests/                   # 存放测试代码
│   ├── __init__.py
│   └── test_reservation.py  # 测试用例
│
├── main.py                  # 主程序入口
└── requirements.txt         # 依赖包列表
```
## 安装依赖

```bash
pip install -r requirements.txt
