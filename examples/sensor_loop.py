"""
OpenRBT Sensor Loop — timer-based publishing at 2Hz.
Run with: python examples/sensor_loop.py
Stop with Ctrl+C.
"""
import openrbt
import random

sensor = openrbt.Node("sensor")
display = openrbt.Node("display")

@display.subscribe("/temperature")
def on_temp(msg):
    print(f"[display] temperature: {msg['value']:.2f}°C")

@sensor.timer(hz=2)
def read_sensor():
    sensor.publish("/temperature", {"value": random.uniform(20.0, 25.0)})

display.spin_once()  # register subscriber
sensor.spin()        # start publishing loop
