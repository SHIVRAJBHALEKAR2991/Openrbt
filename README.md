# OpenRBT

A simple, beginner-friendly robotics communication library for Python.
Inspired by ROS2 but designed to just work — no DDS, no XML, no setup hell.

---

## Why OpenRBT?

ROS2 is powerful but demands hours of setup, XML configs, and a steep learning curve before anything moves. OpenRBT strips that down to a single Python install. Two nodes can exchange messages in under 10 lines — no middleware, no environment variables, no colcon.

---

## Installation

**Future (PyPI):**
```bash
pip install openrbt
```

**Local development:**
```bash
git clone https://github.com/your-org/openrbt
cd openrbt
pip install -e .
```

---

## Quick Start

```python
import openrbt

talker = openrbt.Node("talker")
listener = openrbt.Node("listener")

@listener.subscribe("/chatter")
def on_message(msg):
    print(f"[listener] received: {msg}")

talker.publish("/chatter", "Hello from OpenRBT!")
talker.publish("/chatter", {"x": 1.0, "y": 2.0, "z": 0.0})
```

**Output:**
```
[openrbt] Node 'talker' initialized
[openrbt] Node 'listener' initialized
[listener] received: Hello from OpenRBT!
[listener] received: {'x': 1.0, 'y': 2.0, 'z': 0.0}
```

---

## Core Concepts

### Nodes

A `Node` is a named participant in your robot's communication network. Each node can publish data, subscribe to data, and run periodic timers. Think of it as a process or component: `"camera_node"`, `"motor_controller"`, `"planner"`.

```python
import openrbt
node = openrbt.Node("my_node")
```

### Topics

Topics are named message channels that always start with `/`. Any node can publish to a topic; any node can subscribe to it. Topics carry any Python object — strings, dicts, lists, dataclasses.

```python
node.publish("/sensor/imu", {"ax": 0.1, "ay": 0.0, "az": 9.8})
```

### Publish / Subscribe

Publishing sends a message; subscribing registers a function to receive it. The decorator `@node.subscribe("/topic")` wires up the function automatically.

```python
sender = openrbt.Node("sender")
receiver = openrbt.Node("receiver")

@receiver.subscribe("/ping")
def on_ping(msg):
    print("Got:", msg)

sender.publish("/ping", "pong")
```

### Timers

A timer fires a function at a fixed rate (in Hz). Decorate with `@node.timer(hz=N)` and call `node.spin()` to start the loop.

```python
import openrbt

sensor = openrbt.Node("sensor")

@sensor.timer(hz=10)
def read():
    sensor.publish("/data", {"value": 42})

sensor.spin()  # runs until Ctrl+C
```

---

## API Reference

### Node

| Method | Description |
|---|---|
| `Node(name, broker=None)` | Create a node. Uses global broker by default. |
| `publish(topic, message)` | Send message to topic (topic must start with `/`). |
| `subscribe(topic)` | Decorator — register function as subscriber. |
| `timer(hz)` | Decorator — register function as a periodic timer. |
| `spin()` | Start timers and block until Ctrl+C. |
| `spin_once()` | Start timers, wait one tick, stop. |
| `shutdown()` | Stop timers, unsubscribe all callbacks. |
| `get_info()` | Return dict with node state summary. |

### Broker

| Method | Description |
|---|---|
| `Broker()` | Create an isolated broker (useful for tests). |
| `subscribe(topic, callback)` | Register a callback. |
| `publish(topic, message)` | Deliver to all subscribers. |
| `unsubscribe(topic, callback)` | Remove a specific callback. |
| `get_topics()` | Sorted list of active topics. |
| `get_subscriber_count(topic)` | Number of subscribers on a topic. |
| `clear()` | Remove all subscribers. |

---

## Milestone Roadmap

### Tier 1 — Foundation
- [x] M1: Core messaging layer (Node, Broker, Timer, pub/sub)
- [x] M2: Message schemas with dataclasses and type validation
- [x] M3: Logging and introspection (topic list, node list, message recording)
- [x] M4: Services (request/response pattern)
- [x] M5: Parameters (node-level key/value config)

### Tier 2 — Transport
- [ ] M6: TCP transport (nodes across processes on same machine)
- [ ] M7: UDP multicast discovery (zero-config node detection)
- [ ] M8: Serialization (JSON, msgpack, protobuf)
- [ ] M9: QoS profiles (reliable, best-effort, latching)
- [ ] M10: Multi-machine networking (LAN communication)

### Tier 3 — Robotics Primitives
- [ ] M11: Standard message types (Pose, Twist, Image, LaserScan, etc.)
- [ ] M12: TF / coordinate frame transforms
- [ ] M13: Action server/client (long-running tasks with feedback)
- [ ] M14: Lifecycle nodes (managed state machine)
- [ ] M15: Bag file recording and playback

### Tier 4 — Tooling
- [ ] M16: CLI — `openrbt topic echo`, `openrbt node info`
- [ ] M17: Web dashboard (live topic visualization in browser)
- [ ] M18: rqt-style graph viewer (node/topic graph)
- [ ] M19: Launch system (start multiple nodes from a config file)
- [ ] M20: Plugin system (load node types dynamically)

### Tier 5 — Simulation & Hardware
- [ ] M21: Simulated time and clock API
- [ ] M22: Hardware abstraction layer (GPIO, I2C, SPI stubs)
- [ ] M23: Gazebo bridge (connect to Gazebo simulator)
- [ ] M24: ROS2 bridge (bidirectional topic forwarding with ROS2)
- [ ] M25: MicroPython port (run openrbt on microcontrollers)

### Tier 6 — Intelligence & Scale
- [ ] M26: Behavior trees integration
- [ ] M27: Distributed parameter server
- [ ] M28: Health monitoring and watchdog timers
- [ ] M29: Security layer (topic-level authentication)
- [ ] M30: Cloud relay (remote robot control via MQTT/WebSocket)
- [ ] M31: Auto-generated Python stubs from `.msg` definition files
- [ ] M32: Full documentation site with interactive examples

---

## Contributing

1. Fork the repo and create a feature branch.
2. Run `pytest tests/` — all tests must pass.
3. Follow the code style: type hints on every function, docstrings on every public method, no external dependencies.
4. Open a PR with a clear description of what changed and why.

---

## License

MIT — see LICENSE file for details.
