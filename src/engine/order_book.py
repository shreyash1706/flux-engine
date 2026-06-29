from engine.order import Order,Side 
from engine.order_list import OrderList 

class OrderBook:
    def __init__(self):
        '''
        Price-Level Maps , used for matching trades , ordered
        keys are prices, values are OrderLists
        '''
        self.bids = {}
        self.asks = {}

        #order ids for O(1) removals , values are order objects 
        self.active_orders = {}

        #top of book trackers 
        self.best_bid = None 
        self.best_ask = None 

    def _add_order_to_book(self, order: Order):
        '''
        Orders not executed to be added to the order book 
        update hashmap and market state 
        '''

        if order.side == Side.BUY:
            #check if price level exist 
            if order.price not in self.bids:
                self.bids[order.price] = OrderList()

            self.bids[order.price].append_order()

            self.active_orders[order.order_id] = order

            if self.best_bid:
                if order.price > self.best_bid:
                    self.best_bid = order.price 
            else:
                self.best_bid = order.price

        else:

            if order.price not in self.asks:
                self.asks[order.price] = OrderList()

            self.asks[order.price].append_order()

            self.active_orders[order.order_id] = order

            if self.best_ask:
                if order.price < self.best_ask:
                    self.best_ask = order.price

            else:
                self.best_ask = order.price 

    def process_order(self, order: Order): 

