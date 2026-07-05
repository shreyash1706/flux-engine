from fastapi import FastAPI, HTTPException 
from pydantic import BaseModel 
from confluent_kafka import Producer
import json 
import uuid 

app = FastAPI(title="Flux Engine Gateway")

class OrderRequest(BaseModel):
    side: int # 1=BUY and 2=SELL
    price: float # use -1 for market order , which then gets converted into inf -inf
    quantity: int

producer = None 

@app.on_event('startup')
async def startup_event():
    global producer 
    conf = {
            'bootstrap.servers': 'localhost:9092',
            }
    producer = Producer(conf)

@app.on_event('shutdown')
async def shutdown_event():
    if producer:
        producer.flush()

def delivery_report(err, msg):
    """ Called once for each message produced to indicate delivery result. """
    if err is not None:
        print(f"[ERROR] Message delivery failed: {err}")
    else:
        print(f"[SUCCESS] Order delivered to {msg.topic()} [{msg.partition()}]")

@app.post("/order")
async def place_order(order: OrderRequest):
    """
    Accepts an order, assigns an ID, and pushes to kafka.
    """
    order_id = uuid.uuid4().hex
    order_dict = {
            "order_id": order_id,
            "side": order.side,
            "price": order.price,
            "quantity": order.quantity
            }
    json_payload = json.dumps(order_dict).encode('utf-8')
    producer.produce('order-ingress', value=json_payload, callback=delivery_report)
    producer.poll(0)

    return {"status": "Accepted", "order_id": order_id}

    


