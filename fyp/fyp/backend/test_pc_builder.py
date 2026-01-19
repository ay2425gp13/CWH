#!/usr/bin/env python3
"""
Test script for PC Builder API with authentic GPT responses
Run this after installing Python and dependencies
"""

import requests
import json

def test_pc_builder_api():
    """Test the PC Builder API with different query types"""

    base_url = "http://localhost:5000/api/pc-builder"

    test_queries = [
        "What are the best CPUs for gaming?",
        "What GPU should I get for gaming?",
        "How much RAM do I need for gaming?",
        "Build me a gaming PC under $1500"
    ]

    print("Testing PC Builder API with authentic GPT responses...")
    print("=" * 60)

    for i, query in enumerate(test_queries, 1):
        print(f"\nTest {i}: {query}")
        print("-" * 40)

        try:
            response = requests.post(base_url, json={"message": query}, timeout=10)

            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    ai_response = data.get("response", "")
                    # Print first 200 characters to avoid too much output
                    print(f"✓ Success: {ai_response[:200]}...")
                    if len(ai_response) > 200:
                        print(f"   (Response truncated, full length: {len(ai_response)} chars)")
                else:
                    print(f"✗ API Error: {data.get('message', 'Unknown error')}")
            else:
                print(f"✗ HTTP Error: {response.status_code}")

        except requests.exceptions.RequestException as e:
            print(f"✗ Request Error: {e}")

    print("\n" + "=" * 60)
    print("Test completed!")

if __name__ == "__main__":
    test_pc_builder_api()