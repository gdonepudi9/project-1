#!/bin/bash

echo "=== Testing Key-Value Store ==="
echo ""

# Test 1: Basic SET and GET
echo "Test 1: Basic SET and GET"
echo -e "SET x 10\nGET x\nEXIT" | python3 store.py
echo ""

# Clean up
rm -f data.db

# Test 2: Multiple operations
echo "Test 2: Multiple SET and GET operations"
echo -e "SET name Alice\nSET age 30\nSET city NYC\nGET name\nGET age\nGET city\nEXIT" | python3 store.py
echo ""

# Test 3: Persistence test
echo "Test 3: Testing persistence across restarts"
echo "First run - setting values:"
echo -e "SET foo bar\nSET test value\nEXIT" | python3 store.py
echo ""
echo "Second run - retrieving values:"
echo -e "GET foo\nGET test\nEXIT" | python3 store.py
echo ""

# Test 4: Overwriting values
echo "Test 4: Last write wins"
echo -e "GET name\nSET name Bob\nGET name\nEXIT" | python3 store.py
echo ""

# Test 5: Non-existent key
echo "Test 5: Getting non-existent key"
echo -e "GET nonexistent\nEXIT" | python3 store.py
echo ""

echo "=== All tests completed ==="
