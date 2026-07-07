import pytest
from src.engine.order import Order, Side 
from src.engine.order_book import OrderBook 
import csv
import os 
import random

def test_deterministic_csv_replay():
    book = OrderBook()

    base_dir = os.path.dirname(os.path.dirname(__file__))
    csv_path = os.path.join(base_dir, 'data', 'sample_orders.csv')

    with open(csv_path, 'r') as file:
        reader = csv.reader(file)

        header = next(reader)
        
        for row in reader:
            order = Order(
                    row[0],
                    Side(int(row[1])),
                    float(row[2]),
                    int(row[3])
            )
            book.process_order(order)
            

    assert book.best_bid == 149.00
    assert book.best_ask == 151.00
    assert book.asks[151.00].volume == 150
    

def test_load_10k():
    book = OrderBook()

    base_dir = os.path.dirname(os.path.dirname(__file__))
    csv_path = os.path.join(base_dir, 'data', 'load_test.csv')

    with open(csv_path, 'r') as file:
        reader = csv.reader(file)

        header = next(reader)
        
        for row in reader:
            order = Order(
                    row[0],
                    Side(int(row[1])),
                    float(row[2]),
                    int(row[3])
            )
            book.process_order(order)
            

    if book.best_bid != None and book.best_ask != None:
        assert book.best_bid < book.best_ask

    if book.asks:
        random_key = random.choice(list(book.asks))

        length = 0
        vol = 0
        
        order = book.asks[random_key].head
        while order is not None:
            length+= 1
            vol += order.quantity
            order = order.next_order

        assert book.asks[random_key].length == length
        assert book.asks[random_key].volume == vol

    total_orders = 0 

    for key in book.asks.keys():
        total_orders += book.asks[key].length

    for key in book.bids.keys():
        total_orders += book.bids[key].length

    assert total_orders == len(book.active_orders)


    print(f"Best Buy price, {book.best_bid}")
    print(f"Best Ask price, {book.best_ask}")

if __name__ == "__main__":
    test_load_10k()



