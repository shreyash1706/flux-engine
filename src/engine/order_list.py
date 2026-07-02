from .order import Order 

class OrderList:
    '''
    new orders added at tail 
    trades happen at head
    upon order cancellation, removal from anywhere in O(1) constant time.
    '''
    def __init__(self):
        self.head = None 
        self.tail = None 
        self.length = 0 
        self.volume = 0 #total quantity at this price point 

    def append_order(self, order: Order):
        '''
        add order to the tail of the linked list 
        update volume and length 
        ''' 
        if self.length == 0 :
            self.head = self.tail = order 

        else:
            self.tail.next_order = order 
            order.prev_order = self.tail 
            self.tail = order 


        self.length += 1 
        self.volume += order.quantity 


    def remove_order(self, order: Order):
        '''
        remove order from anywhere 
        patch pointers 
        update volume and length 
        '''

        #case1: only order in the list 
        if self.length == 1:
            self.head = None 
            self.tail = None 

        #case2: order at front 
        elif order == self.head : 
            self.head = order.next_order
            order.next_order = None
            self.head.prev_order = None 

        #case3: order at back 
        elif order == self.tail: 
            self.tail = order.prev_order
            order.prev_order = None
            self.tail.next_order = None 

        #case4: order in middle 
        else:
            order.prev_order.next_order = order.next_order
            order.next_order.prev_order = order.prev_order
            order.next_order = order.prev_order = None 

        self.length -= 1 
        self.volume -= order.quantity
            
        




