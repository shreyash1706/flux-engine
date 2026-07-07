from fastapi import FastAPI, HTTPException,WebSocket, WebSocketDisconnect 
import redis.asyncio as aioredis
import asyncio
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

@app.websocket("/stream")
async def websocket_endpoint(websocket: WebSocket):
    #accept connection from user's browser
    await websocket.accept()

    redis_client = await aioredis.Redis(host='localhost', port = 6379, db=0)

    pubsub = redis_client.pubsub()

    pubsub.subscribe("market_updates")

    try: 
        while True:
            #wait for msg from redis 
            message = await pubsub.get_message(ignore_subscribe_message=True, timeout = 1.0)
            if message is not None:
                #extract data
                raw_data = message['data'].decode('utf-8')

                await websocket.send_text(raw_data)

            await asyncio.sleep(0.01)

    except WebSocketDisconnect:
        print("Client disconnected from stream")
    finally:
        await pubsub.unsubscribe('market_updates')
        await redis_client.close()


