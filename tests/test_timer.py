"""Tests for openrbt.timer.Timer."""

import time
import pytest
from openrbt.timer import Timer


def test_timer_fires():
    count = []
    t = Timer(hz=10, callback=lambda: count.append(1))
    t.start()
    time.sleep(0.5)
    t.stop()
    assert len(count) >= 3


def test_timer_stop():
    count = []
    t = Timer(hz=20, callback=lambda: count.append(1))
    t.start()
    time.sleep(0.2)
    t.stop()
    snapshot = len(count)
    time.sleep(0.2)
    assert len(count) == snapshot


def test_timer_is_running():
    t = Timer(hz=10, callback=lambda: None)
    assert not t.is_running()
    t.start()
    assert t.is_running()
    t.stop()
    assert not t.is_running()


def test_timer_exception_doesnt_crash():
    count = []

    def bad_cb():
        count.append(1)
        raise RuntimeError("intentional error")

    t = Timer(hz=20, callback=bad_cb, node_name="test_node")
    t.start()
    time.sleep(0.3)
    t.stop()
    assert len(count) >= 2
