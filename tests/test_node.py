"""Tests for openrbt.node.Node."""

import pytest
from openrbt.broker import Broker, _global_broker
from openrbt.node import Node


@pytest.fixture(autouse=True)
def reset_broker():
    _global_broker.clear()
    yield
    _global_broker.clear()


def test_node_init():
    n = Node("robot")
    assert n.name == "robot"


def test_publish_subscribe():
    a = Node("talker")
    b = Node("listener")
    received = []

    @b.subscribe("/msg")
    def on_msg(m):
        received.append(m)

    a.publish("/msg", "hi")
    assert received == ["hi"]


def test_invalid_topic_publish():
    n = Node("n")
    with pytest.raises(ValueError, match="must start with '/'"):
        n.publish("no_slash", "data")


def test_invalid_topic_subscribe():
    n = Node("n")
    with pytest.raises(ValueError, match="must start with '/'"):

        @n.subscribe("no_slash")
        def cb(m):
            pass


def test_multiple_nodes_same_broker():
    a = Node("a")
    b = Node("b")
    c = Node("c")
    log = []

    @b.subscribe("/shared")
    def on_b(m):
        log.append(("b", m))

    @c.subscribe("/shared")
    def on_c(m):
        log.append(("c", m))

    a.publish("/shared", 1)
    assert ("b", 1) in log
    assert ("c", 1) in log


def test_node_shutdown_cleans_up():
    a = Node("pub")
    b = Node("sub")
    received = []

    @b.subscribe("/t")
    def on_t(m):
        received.append(m)

    b.shutdown()
    a.publish("/t", "after-shutdown")
    assert received == []


def test_get_info():
    n = Node("info_node")

    @n.subscribe("/x")
    def cb(m):
        pass

    info = n.get_info()
    assert info["name"] == "info_node"
    assert "/x" in info["subscriptions"]
    assert info["timers"] == 0
    assert info["running"] is False


def test_spin_once():
    n = Node("spinner")
    fired = []

    @n.timer(hz=100)
    def tick():
        fired.append(1)

    n.spin_once()
    assert len(fired) >= 1
