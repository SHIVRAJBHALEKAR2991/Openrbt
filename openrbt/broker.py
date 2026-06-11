"""Broker — central pub/sub message bus for OpenRBT."""

from __future__ import annotations


class Broker:
    """Central message broker that routes published messages to subscribers."""

    def __init__(self) -> None:
        self._subscribers: dict[str, list[callable]] = {}

    def subscribe(self, topic: str, callback: callable) -> None:
        """Register a callback to receive messages on topic."""
        if topic not in self._subscribers:
            self._subscribers[topic] = []
        self._subscribers[topic].append(callback)

    def publish(self, topic: str, message: any) -> None:
        """Deliver message to all subscribers on topic; silent if none."""
        for cb in self._subscribers.get(topic, []):
            cb(message)

    def unsubscribe(self, topic: str, callback: callable) -> None:
        """Remove a specific callback from topic; silent if not found."""
        if topic in self._subscribers:
            try:
                self._subscribers[topic].remove(callback)
            except ValueError:
                pass

    def get_topics(self) -> list[str]:
        """Return sorted list of topics that have at least one subscriber."""
        return sorted(t for t, cbs in self._subscribers.items() if cbs)

    def get_subscriber_count(self, topic: str) -> int:
        """Return number of subscribers for topic, 0 if unknown."""
        return len(self._subscribers.get(topic, []))

    def clear(self) -> None:
        """Remove all subscribers from all topics."""
        self._subscribers.clear()


_global_broker = Broker()
