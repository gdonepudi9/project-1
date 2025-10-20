import sys
import os

db_file = "data.db"
store = {}

# Load existing data from file
if os.path.exists(db_file):
    with open(db_file, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                parts = line.split(" ", 1)
                if len(parts) == 2:
                    key = parts[0]
                    value = parts[1]
                    store[key] = value

# Main loop
while True:
    try:
        user_input = input().strip()
    except EOFError:
        break
    
    if not user_input:
        continue
    
    parts = user_input.split(" ", 1)
    command = parts[0].upper()
    
    if command == "SET":
        if len(parts) < 2:
            print("ERROR: SET requires key and value")
            continue
        
        args = parts[1].split(" ", 1)
        if len(args) < 2:
            print("ERROR: SET requires key and value")
            continue
        
        key = args[0]
        value = args[1]
        
        store[key] = value
        
        # Write to file immediately
        with open(db_file, "a") as f:
            f.write(f"{key} {value}\n")
        
        print(f"SET {key} = {value}")
    
    elif command == "GET":
        if len(parts) < 2:
            print("ERROR: GET requires key")
            continue
        
        key = parts[1].strip()
        
        if key in store:
            print(store[key])
        else:
            print("NULL")
    
    elif command == "EXIT":
        break
    
    else:
        print(f"ERROR: Unknown command {command}")
