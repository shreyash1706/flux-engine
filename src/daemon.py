from confluent_kafka import Consumer, KafkaError 
import redis 
import json 
from src.engine.order_book import OrderBook 
from src.engine.order import Order,Side 


def run_daemon():
    print("Starting Flux Engine Daemon...")

    book = OrderBook()

    cache = redis.Redis(host='localhost', port= 6379, db=0)

    conf ={
            'bootstrap.servers':'localhost:9092',
            'group.id':'flux-engine-core',
            'auto.offset.reset':'earliest'
        }
    consumer = Consumer(conf)
    
    consumer.subscribe(['order-ingress'])
    print("Listening for orders on 'order-ingress'...")

    try:
        while True:
            msg = consumer.poll(1.0)

            if msg is None:
                continue
            if msg.error():
                print(f"Consumer error: {msg.error()}")
                continue

            
            #Extract raw bytes 
            raw_bytes = msg.value()
            order_dict = json.loads(raw_bytes.decode('utf-8'))

            order = Order(
                    order_dict['order_id'],
                    Side(int(order_dict['side'])),
                    float(order_dict['price']),
                    int(order_dict['quantity'])
            )
            book.process_order(order)
 
            publish_state_to_redis(book, cache)
            print(f"Processed order {order.order_id}, updated state in Redis.")

    except KeyboardInterrupt:
        print("Shutting down daemon...")
    finally:
        consumer.close()

def publish_state_to_redis(book: OrderBook , cache: redis.Redis):
    """
    Takes current state of the book and writes a snapshot to redis.
    """
    bid_vol = book.bids[book.best_bid].volume if book.best_bid is not None else 0
    ask_vol = book.asks[book.best_ask].volume if book.best_ask is not None else 0

    state_dict ={
            "best_bid" : book.best_bid,
            "best_bid_volume": bid_vol,
            "best_ask" : book.best_ask,
            "best_ask_volume": ask_vol
        }
    cache.set("market_state", json.dumps(state_dict))

if __name__ == "__main__":
    run_daemon()





