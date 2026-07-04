# data/generate_load.py
import csv
import os
import random

def generate_market_load(filename="load_test.csv", num_orders=10000):
    # Establish the path to deposit the file straight into your data folder
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir, filename)
    
    anchor_price = 100.00
    
    print(f"Generating {num_orders} orders at {csv_path}...")
    
    with open(csv_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Write the exact headers your engine expects
        writer.writerow(["order_id", "side", "price", "quantity"])
        
        for i in range(1, num_orders + 1):
            order_id = f"LOD_{i}"
            
            # 1 = Buy, 2 = Sell (Matching the FIX protocol standard we set up)
            side = random.choice([1, 2])
            
            # Generate a realistic price centered around $100 within a tight spread
            # Rounded to 2 decimal places for typical stock pricing
            price_delta = random.uniform(-5.00, 5.00)
            price = round(anchor_price + price_delta, 2)
            
            # Quantities ranging from small retail clips to mid-size institutional blocks
            quantity = random.randint(10, 500)
            
            writer.writerow([order_id, side, price, quantity])
            
    print("Generation complete! Ready for stress testing.")

if __name__ == "__main__":
    generate_market_load()
