import pytest 
from src.engine.order import Order, Side 
from src.engine.order import OrderBook

@pytest.fixture
def empty_book():
    return OrderBook()

def test_simple_insert(empty_book):
    order = Order("1",Side.BUY, 150.00, 100)
    empty_book.process_order(order)

    assert empty_book.best_bid == 150.00
    assert empty_book.bids[150.0].volume == 100 
    assert empty_book.best_ask is None
