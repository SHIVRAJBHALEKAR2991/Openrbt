"""Timer — runs a callback at a fixed rate in a background thread."""

from __future__ import annotations
import threading
import time


class Timer:
    """Calls callback at hz times per second using a daemon background thread."""

    def __init__(self, hz: float, callback: callable, node_name: str = "") -> None:
        self._interval = 1.0 / hz
        self._callback = callback
        self._node_name = node_name
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None

    def start(self) -> None:
        """Start the background timer thread."""
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def _run(self) -> None:
        while not self._stop_event.wait(self._interval):
            try:
                self._callback()
            except Exception as e:
                print(f"[openrbt] Timer exception in node '{self._node_name}': {e}")

    def stop(self) -> None:
        """Signal the thread to stop and wait up to 1 second for it to finish."""
        self._stop_event.set()
        if self._thread is not None:
            self._thread.join(timeout=1.0)

    def is_running(self) -> bool:
        """Return True if the timer thread is alive."""
        return self._thread is not None and self._thread.is_alive()
