import pytest 
from src.engine.order import Order, Side 
from src.engine.order_book import OrderBook

@pytest.fixture
def empty_book():
    return OrderBook()

def test_simple_insert(empty_book):
    order = Order("1",Side.BUY, 150.00, 100)
    empty_book.process_order(order)

    assert empty_book.best_bid == 150.00
    assert empty_book.bids[150.0].volume == 100 
    assert empty_book.best_ask is None


def test_order_execution(empty_book):
    order = Order("1", Side.SELL, 100.00, 10)
    empty_book.process_order(order)
    order = Order("2", Side.BUY, 110.00, 10)
    empty_book.process_order(order)

    assert empty_book.bids == {}
    assert empty_book.asks == {}


def test_partial_fill(empty_book):
    order = Order("1",Side.SELL, 150.00, 50)
    empty_book.process_order(order)
    order = Order("2",Side.BUY, 150.00, 20)
    empty_book.process_order(order)

    
    assert empty_book.bids == {}
    assert empty_book.asks[150.00].volume == 30 

def test_multi_level_sweep(empty_book):
    order = Order("1",Side.SELL, 150.00, 50)
    empty_book.process_order(order)
    order = Order("2",Side.SELL, 155.00, 50)
    empty_book.process_order(order)
    order = Order("3",Side.BUY, 160.00, 80)
    empty_book.process_order(order)

    assert empty_book.best_ask == 155
    assert "1" not in empty_book.active_orders
    assert empty_book.active_orders["2"].quantity == 20 

def test_cancel_order_via_active_map(empty_book):

    order = Order("1", Side.BUY, 100, 100 )
    empty_book.process_order(order)
    empty_book.bids[100.0].remove_order(empty_book.active_orders["1"])

    assert empty_book.bids[100.0].length == 0 

    
def test_fifo_time_priority(empty_book):
    order = Order("1",Side.SELL, 150.00, 100)
    empty_book.process_order(order)
    order = Order("2",Side.SELL, 150.00, 100)
    empty_book.process_order(order)
    order = Order("3",Side.BUY, 150.00, 100)
    empty_book.process_order(order)

    assert "1" not in empty_book.active_orders
    assert empty_book.active_orders["2"].quantity == 100

def test_market_order(empty_book):

    order = Order("1",Side.SELL, 150.00, 50)
    empty_book.process_order(order)
    order = Order("2",Side.SELL, 155.00, 50)
    empty_book.process_order(order)
    order = Order("3",Side.BUY, float('inf'), 80)
    empty_book.process_order(order)
 
    assert empty_book.best_ask == 155
    assert "1" not in empty_book.active_orders
    assert empty_book.active_orders["2"].quantity == 20 


def test_market_kill_switch(empty_book):

    order = Order("1", Side.SELL, 150 , 10 )
    empty_book.process_order(order)
    order = Order("2", Side.BUY, float('inf'), 100)
    empty_book.process_order(order)
    
    assert empty_book.bids == {}


        
