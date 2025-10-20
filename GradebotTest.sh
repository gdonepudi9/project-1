#!/bin/bash
# Test script for the key-value store

echo "========================================="
echo "Testing Simple Key-Value Store"
echo "========================================="

# Clean up any existing database
rm -f data.db

echo ""
echo "Test 1: Basic SET and GET"
echo "-----------------------------------------"
echo -e "SET name Alice\nGET name\nEXIT" | python3 store.py

echo ""
echo "Test 2: Multiple operations"
echo "-----------------------------------------"
echo -e "SET x 10\nSET y 20\nGET x\nGET y\nEXIT" | python3 store.py

echo ""
echo "Test 3: Last write wins"
echo "-----------------------------------------"
echo -e "SET key value1\nSET key value2\nGET key\nEXIT" | python3 store.py

echo ""
echo "Test 4: Persistence test (two runs)"
echo "-----------------------------------------"
echo "Run 1 - Setting values:"
echo -e "SET persistent data123\nEXIT" | python3 store.py

echo ""
echo "Run 2 - Reading after restart:"
echo -e "GET persistent\nEXIT" | python3 store.py

echo ""
echo "Test 5: Values with spaces"
echo "-----------------------------------------"
echo -e "SET greeting Hello World\nGET greeting\nEXIT" | python3 store.py

echo ""
echo "========================================="
echo "All tests completed!"
echo "========================================="

# Clean up
rm -f data.db
