import json
import urllib.request
import urllib.error
import sys
import time

NODES = {
    "leader": "http://localhost:8080",
    "follower-1": "http://localhost:8081",
    "follower-2": "http://localhost:8082",
}


def post_data(node, key, value):
    url = f"{NODES[node]}/data"

    payload = json.dumps({
        "key": key,
        "value": value
    }).encode("utf-8")

    request = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(request, timeout=3) as response:
            result = response.read().decode("utf-8")
            print(f"[OK] {node}: {result}")
    except Exception as e:
        print(f"[ERROR] {node}: {e}")


def get_data(node):
    url = f"{NODES[node]}/data"

    try:
        with urllib.request.urlopen(url, timeout=3) as response:
            result = response.read().decode("utf-8")
            print(f"[{node}] {result}")
    except Exception as e:
        print(f"[ERROR] {node}: {e}")


def health(node):
    url = f"{NODES[node]}/health"

    try:
        with urllib.request.urlopen(url, timeout=3) as response:
            result = response.read().decode("utf-8")
            print(f"[{node}] {result}")
    except Exception as e:
        print(f"[ERROR] {node}: {e}")


def main():
    print("=== Distributed Replication Load Test ===")

    print("\n--- Health des nœuds ---")
    for node in NODES:
        health(node)

    print("\n--- Envoi de order-1 au Leader ---")
    post_data(
        "leader",
        "order-1",
        "Laptop - quantity=2 - price=1200"
    )

    time.sleep(1)

    print("\n--- Vérification des données ---")
    for node in NODES:
        get_data(node)


if __name__ == "__main__":
    main()