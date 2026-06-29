from engine.order import Order 

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
        self.volume = 1 #total quantity at this price point 

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


        
