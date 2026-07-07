#End to End Integration test for engine , kafka and redis .
import pytest 
import requests
import csv
import os 
import redis
import time 
import json 
from concurrent.futures import ThreadPoolExecutor 

API_URL = "http://localhost:8000/order"

def fire_request(row):
    requests.post(API_URL, json={
        'side' : int(row[1]),
        'price' : float(row[2]),
        'quantity' : int(row[3])
        })

def test_full_system_pipeline():
    
    base_dir = os.path.dirname(os.path.dirname(__file__))
    csv_path = os.path.join(base_dir, 'data', 'load_test.csv')
    orders_to_send = [] 


    with open(csv_path, 'r') as file:
        reader = csv.reader(file)

        header = next(reader)
        
        for row in reader:

            orders_to_send.append(row)

    print(f"Loaded {len(orders_to_send)} orders. Blasting API...")
    #multi-threaded blaster upto 100 requests simultaneously to stress the API
    with ThreadPoolExecutor(max_workers=100) as executor:
        executor.map(fire_request, orders_to_send)

    print("All requests fired! Waiting for Daemon to drain the Kafka queue...")

    time.sleep(3) 

    
    cache = redis.Redis(host='localhost', port= 6379, db=0)

    state_dict = json.loads(cache.get("market_state").decode('utf-8'))

        # Ensure we got valid numbers back
    assert state_dict["best_bid"] is not None
    assert state_dict["best_ask"] is not None

    # The golden rule of order books: The bid must NEVER cross the ask!
    assert state_dict["best_bid"] < state_dict["best_ask"]

    # Ensure volumes are positive integers
    assert state_dict["best_bid_volume"] > 0

