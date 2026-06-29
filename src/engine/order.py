from time import time_ns 
from enum import Enum 

class Side(Enum):
    '''
    Using Enum for cleaner code and for understandable implementation of logic
    Buy and sell, uses 1 and 2 for disambiguation from true/false. and industry FIX tags follow these.
    '''
    BUY = 1
    SELL = 2

class order:
    def __init__(self, order_id: str, side: Side, price: float, quantity: int):
        self.order_id = order_id 
        self.side = side
        self.price = price
        self.quantity = quantity
        self.timestamp = time_ns()

        #pointers for Doubly linked list 
        self.next_order = None
        self.prev_order = None

    def __repr__(self):
        return f"Order({self.order_id}, {self.side.name}, {self.price}, {self.quantity})"
        
