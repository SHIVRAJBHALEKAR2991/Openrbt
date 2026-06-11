"""
OpenRBT Hello World — two nodes exchanging a message.
Run with: python examples/hello_world.py
"""
import openrbt

talker = openrbt.Node("talker")
listener = openrbt.Node("listener")

@listener.subscribe("/chatter")
def on_message(msg):
    print(f"[listener] received: {msg}")

talker.publish("/chatter", "Hello from OpenRBT!")
talker.publish("/chatter", {"x": 1.0, "y": 2.0, "z": 0.0})
