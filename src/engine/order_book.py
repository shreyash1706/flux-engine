from .order import Order,Side 
from .order_list import OrderList 

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

            self.bids[order.price].append_order(order)

            self.active_orders[order.order_id] = order

            if self.best_bid:
                if order.price > self.best_bid:
                    self.best_bid = order.price 
            else:
                self.best_bid = order.price

        else:

            if order.price not in self.asks:
                self.asks[order.price] = OrderList()

            self.asks[order.price].append_order(order)

            self.active_orders[order.order_id] = order

            if self.best_ask:
                if order.price < self.best_ask:
                    self.best_ask = order.price

            else:
                self.best_ask = order.price 

    def process_order(self, order: Order): 
        '''
        trade processing 
        checking if orders cross the spread to make it happen.
        '''

        if order.side == Side.BUY and self.best_ask != None and order.price >= self.best_ask:
            while order.quantity > 0 and self.best_ask is not None and order.price >= self.best_ask: 
                
                target_order = self.asks[self.best_ask].head
                trade_volume = min(target_order.quantity, order.quantity)    
                order.quantity -= trade_volume
                target_order.quantity -= trade_volume
                self.asks[self.best_ask].volume -= trade_volume
                
                # Inside your while loop, right after calculating trade_volume:
                print(f"[TRADE EXECUTION] Order {order.order_id} matched with {target_order.order_id} | Qty: {trade_volume} @ ${self.best_ask}")

                if target_order.quantity <= 0 :
                    del self.active_orders[target_order.order_id]
                    self.asks[self.best_ask].remove_order(target_order)
                    
                    if self.asks[self.best_ask].length == 0  :
                        del self.asks[self.best_ask]
                        if self.asks:
                            self.best_ask = min(self.asks)
                        else:
                            self.best_ask = None


        elif order.side == Side.SELL and self.best_bid is not None and order.price <= self.best_bid:

            while order.quantity > 0 and self.best_bid is not None and order.price <= self.best_bid:
                target_order = self.bids[self.best_bid].head
                trade_volume = min(target_order.quantity, order.quantity)    
                order.quantity -= trade_volume
                target_order.quantity -= trade_volume
                self.bids[self.best_bid].volume -= trade_volume

                # Inside your while loop, right after calculating trade_volume:
                print(f"[TRADE EXECUTION] Order {order.order_id} matched with {target_order.order_id} | Qty: {trade_volume} @ ${self.best_bid}")


                if target_order.quantity <= 0:
                    del self.active_orders[target_order.order_id]
                    self.bids[self.best_bid].remove_order(target_order)

                    if self.bids[self.best_bid].length == 0:
                        del self.bids[self.best_bid] 
                        if self.bids:
                            self.best_bid = max(self.bids)
                        else: 
                            self.best_bid = None

        if order.quantity > 0 :
            if order.price == float('inf') or order.price == float('-inf'):
                print("Market Order Killed")
            else:
                self._add_order_to_book(order)


def cancel_order(self, order_id: str):
    '''
    Manual cancellation endpoint.
    removes resting orders directly without trading.
    '''
    if order_id not in self.active_orders:
        return 

    order_to_cancel = self.active_orders[order_id]
    price = order_to_cancel.price

    if order_to_cancel.side == Side.BUY:

        self.bids[price].remove_order(order_to_cancel)
        del self.active_orders[order_id]

        if self.bids[price].length == 0 :
            del self.bids[price]
            if self.bids:
                self.best_bid = max(self.bids)
            else:
                self.best_bid = None


    else:

        self.asks[price].remove_order(order_to_cancel)
        del self.active_orders[order_id]

        if self.asks[price].length == 0 :
            del self.asks[price]
            if self.asks:
                self.best_ask = min(self.asks)
            else:
                self.best_ask = None



