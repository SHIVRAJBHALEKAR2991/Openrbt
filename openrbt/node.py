"""Node — the primary user-facing object for OpenRBT."""

from __future__ import annotations
import time
from .broker import Broker, _global_broker
from .timer import Timer


class Node:
    """A named participant in the OpenRBT pub/sub network."""

    def __init__(self, name: str, broker: Broker | None = None) -> None:
        self.name = name
        self.broker = broker if broker is not None else _global_broker
        self._timers: list[Timer] = []
        self._subscriptions: list[tuple[str, callable]] = []
        self._running: bool = False
        print(f"[openrbt] Node '{self.name}' initialized")

    def publish(self, topic: str, message: any) -> None:
        """Publish message to topic. Topic must start with '/'."""
        self._validate_topic(topic)
        self.broker.publish(topic, message)

    def subscribe(self, topic: str) -> callable:
        """Decorator factory — register the decorated function as a subscriber."""
        self._validate_topic(topic)

        def decorator(fn: callable) -> callable:
            self.broker.subscribe(topic, fn)
            self._subscriptions.append((topic, fn))
            return fn

        return decorator

    def timer(self, hz: float) -> callable:
        """Decorator factory — wrap the decorated function in a Timer at hz."""
        def decorator(fn: callable) -> callable:
            t = Timer(hz=hz, callback=fn, node_name=self.name)
            self._timers.append(t)
            return fn

        return decorator

    def spin(self) -> None:
        """Start all timers and block until Ctrl+C."""
        self._running = True
        for t in self._timers:
            t.start()
        print(f"[openrbt] Node '{self.name}' spinning. Press Ctrl+C to stop.")
        try:
            while self._running:
                time.sleep(0.1)
        except KeyboardInterrupt:
            self.shutdown()

    def spin_once(self) -> None:
        """Start timers, sleep one tick, then stop — non-blocking helper."""
        for t in self._timers:
            t.start()
        time.sleep(0.1)
        for t in self._timers:
            t.stop()

    def shutdown(self) -> None:
        """Stop timers, unsubscribe all callbacks, mark node as not running."""
        self._running = False
        for t in self._timers:
            t.stop()
        for topic, fn in self._subscriptions:
            self.broker.unsubscribe(topic, fn)
        print(f"[openrbt] Node '{self.name}' shut down.")

    def get_info(self) -> dict:
        """Return a summary dict of this node's current state."""
        return {
            "name": self.name,
            "subscriptions": [topic for topic, _ in self._subscriptions],
            "timers": len(self._timers),
            "running": self._running,
        }

    @staticmethod
    def _validate_topic(topic: str) -> None:
        if not topic.startswith("/"):
            raise ValueError(f"Topic names must start with '/', got: {topic}")
