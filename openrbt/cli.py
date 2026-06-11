"""Minimal CLI stub for OpenRBT."""

from __future__ import annotations
import argparse
from .broker import _global_broker
from . import __version__


def main() -> None:
    """Entry point for the openrbt CLI."""
    parser = argparse.ArgumentParser(prog="openrbt", description="OpenRBT CLI")
    parser.add_argument("--version", action="version", version=f"openrbt {__version__}")
    sub = parser.add_subparsers(dest="command")

    node_p = sub.add_parser("node", help="Node commands")
    node_p.add_argument("action", choices=["list"])

    topic_p = sub.add_parser("topic", help="Topic commands")
    topic_p.add_argument("action", choices=["list"])

    args = parser.parse_args()

    if args.command == "node":
        print("[openrbt] No nodes running. Start a node first.")
    elif args.command == "topic":
        topics = _global_broker.get_topics()
        if topics:
            for t in topics:
                print(t)
        else:
            print("[openrbt] No active topics.")
    else:
        parser.print_help()
