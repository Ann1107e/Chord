# File: chord_full.py

import hashlib
import random
import time

# Kích thước không gian định danh (2^m)
m = 6
MAX_ID = 2**m

def hash_key(key):
    """Hàm băm trả về giá trị trong không gian m-bit."""
    return int(hashlib.sha1(str(key).encode()).hexdigest(), 16) % MAX_ID

def in_range(x, a, b, inclusive=True):
    """Kiểm tra xem x có nằm trong khoảng (a, b] không."""
    if a < b:
        return a < x <= b if inclusive else a < x < b
    else:  # Trường hợp a > b (vòng tròn bị "vượt qua")
        return x > a or x <= b if inclusive else x > a or x < b

class Node:
    def __init__(self, node_id):
        self.id = node_id
        self.successor = self
        self.predecessor = None
        self.finger = [self] * m
        
    def find_successor(self, key_id):
        """Tìm node chịu trách nhiệm cho một khóa bằng finger table."""
        if in_range(key_id, self.id, self.successor.id, inclusive=True):
            return self.successor
        
        n0 = self.closest_preceding_node(key_id)
        if n0 == self:
            return self.successor.find_successor(key_id)
        return n0.find_successor(key_id)
    
    def closest_preceding_node(self, key_id):
        """Tìm node gần nhất (trước key_id) trong finger table."""
        for i in reversed(range(m)):
            finger_node = self.finger[i]
            if finger_node and in_range(finger_node.id, self.id, key_id, inclusive=False):
                return finger_node
        return self
        
    def join(self, start_node):
        """Node mới tham gia vào vòng tròn."""
        if start_node:
            self.successor = start_node.find_successor(self.id)
            self.predecessor = self.successor.predecessor
            if self.predecessor:
                self.predecessor.successor = self
            self.successor.predecessor = self
        else: # Node đầu tiên
            self.predecessor = self
            
    def update_finger_table(self):
        """Cập nhật finger table."""
        for i in range(m):
            start = (self.id + 2**i) % MAX_ID
            self.finger[i] = self.find_successor(start)
    
def create_chord_ring(num_nodes, node_ids=None):
    """Tạo vòng tròn Chord đầy đủ."""
    if node_ids is None:
        ids = sorted([hash_key(i) for i in range(num_nodes)])
    else:
        ids = sorted(node_ids)

    nodes = []
    
    # Tạo node đầu tiên và đặt predecessor của nó là chính nó
    first_node = Node(ids[0])
    first_node.predecessor = first_node
    nodes.append(first_node)
    
    # Chèn các node còn lại
    for i in range(1, len(ids)):
        new_node = Node(ids[i])
        new_node.join(first_node)
        nodes.append(new_node)
    
    # Cập nhật lại các liên kết predecessor/successor một lần nữa để đảm bảo tính nhất quán
    for i in range(len(nodes)):
        nodes[i].successor = nodes[(i + 1) % len(nodes)]
    for i in range(len(nodes)):
        nodes[i].predecessor = nodes[(i - 1 + len(nodes)) % len(nodes)]
        
    # Cập nhật finger table cho tất cả các node
    for n in nodes:
        n.update_finger_table()
            
    return nodes