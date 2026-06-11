"""Tests for openrbt.broker.Broker."""

import pytest
from openrbt.broker import Broker


@pytest.fixture(autouse=True)
def fresh_broker():
    """Each test gets a fresh broker instance."""
    return  # tests create their own brokers


def make_broker() -> Broker:
    return Broker()


def test_subscribe_and_publish():
    b = make_broker()
    received = []
    b.subscribe("/a", received.append)
    b.publish("/a", "hello")
    assert received == ["hello"]


def test_multiple_subscribers():
    b = make_broker()
    r1, r2 = [], []
    b.subscribe("/a", r1.append)
    b.subscribe("/a", r2.append)
    b.publish("/a", 42)
    assert r1 == [42]
    assert r2 == [42]


def test_no_subscriber_no_crash():
    b = make_broker()
    b.publish("/nonexistent", "data")  # must not raise


def test_unsubscribe():
    b = make_broker()
    received = []
    b.subscribe("/a", received.append)
    b.unsubscribe("/a", received.append)
    b.publish("/a", "msg")
    assert received == []


def test_get_topics():
    b = make_broker()
    b.subscribe("/z", lambda m: None)
    b.subscribe("/a", lambda m: None)
    b.subscribe("/m", lambda m: None)
    assert b.get_topics() == ["/a", "/m", "/z"]


def test_get_subscriber_count():
    b = make_broker()
    cb = lambda m: None
    b.subscribe("/x", cb)
    b.subscribe("/x", cb)
    assert b.get_subscriber_count("/x") == 2
    assert b.get_subscriber_count("/missing") == 0


def test_clear():
    b = make_broker()
    received = []
    b.subscribe("/a", received.append)
    b.clear()
    b.publish("/a", "after clear")
    assert received == []


def test_topic_isolation():
    b = make_broker()
    got_a, got_b = [], []
    b.subscribe("/a", got_a.append)
    b.subscribe("/b", got_b.append)
    b.publish("/a", "only-a")
    assert got_a == ["only-a"]
    assert got_b == []
