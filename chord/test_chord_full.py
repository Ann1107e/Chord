# File: test_chord_full.py

import random
from chord_full import create_chord_ring, Node

def run_tests():
    """Chạy tất cả các test case."""
    # Tạo vòng tròn với các ID cố định để đảm bảo kết quả nhất quán
    node_ids = [7, 23, 40, 52, 60]
    nodes = create_chord_ring(len(node_ids), node_ids)

    # In thông tin Finger Table để kiểm tra
    print("--- Trạng thái Vòng tròn và Finger Table ---")
    for n in nodes:
        print(f"\nNode ID: {n.id}")
        print(f"  - Successor: {n.successor.id}")
        print(f"  - Predecessor: {n.predecessor.id}")
        print("  - Finger Table:")
        for i, finger_node in enumerate(n.finger):
            print(f"    * {i + 1}: Start={(n.id + 2**i) % 64:<2} -> {finger_node.id}")
    print("\n" + "="*50 + "\n")

    test_cases = [
        {"name": "1. Key nằm giữa node và successor", "start_node_id": 7, "key_id": 30, "expected_id": 40},
        {"name": "2. Key nhỏ hơn tất cả node", "start_node_id": 60, "key_id": 5, "expected_id": 7},
        {"name": "3. Key lớn hơn tất cả node", "start_node_id": 40, "key_id": 63, "expected_id": 7},
        {"name": "4. Key trùng ID với node", "start_node_id": 7, "key_id": 40, "expected_id": 40},
        {"name": "5. Lookup bắt đầu từ node khác", "start_node_id": 52, "key_id": 18, "expected_id": 23}
    ]

    for case in test_cases:
        start_node = next((n for n in nodes if n.id == case["start_node_id"]), None)
        
        print(f"----------------------------------------------------")
        print(f"Test Case: {case['name']}")
        print(f"  - Key ID: {case['key_id']}")
        print(f"  - Bắt đầu tìm kiếm từ node: {start_node.id}")
        
        # Gọi find_successor của phiên bản đầy đủ
        actual_succ = start_node.find_successor(case['key_id'])

        print(f"  - Kết quả thực tế: Key được lưu tại node {actual_succ.id}")
        print(f"  - Kết quả kỳ vọng: Key được lưu tại node {case['expected_id']}")
        
        if actual_succ.id == case['expected_id']:
            print("  ✅ PASS: Kết quả khớp với kỳ vọng!")
        else:
            print("  ❌ FAIL: Kết quả không khớp với kỳ vọng.")

if __name__ == "__main__":
    run_tests()