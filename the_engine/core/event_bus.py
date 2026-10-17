"""
The Engine - Internal Event Bus & Audit Stream
Provides synchronous and queued messaging between agents with complete audit logs.
"""

from typing import Dict, Any, List, Callable
from datetime import datetime
import logging
from the_engine.config import get_utc_iso

logger = logging.getLogger("TheEngine.EventBus")


class Event:
    def __init__(self, topic: str, sender: str, payload: Dict[str, Any]):
        self.topic = topic
        self.sender = sender
        self.payload = payload
        self.timestamp = get_utc_iso()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "topic": self.topic,
            "sender": self.sender,
            "payload": self.payload,
            "timestamp": self.timestamp
        }


class EventBus:
    def __init__(self):
        self.subscribers: Dict[str, List[Callable[[Event], None]]] = {}
        self.history: List[Event] = []

    def subscribe(self, topic: str, handler: Callable[[Event], None]) -> None:
        if topic not in self.subscribers:
            self.subscribers[topic] = []
        self.subscribers[topic].append(handler)

    def publish(self, topic: str, sender: str, payload: Dict[str, Any]) -> Event:
        event = Event(topic, sender, payload)
        self.history.append(event)
        logger.debug(f"Event: [{topic}] from {sender}")

        if topic in self.subscribers:
            for handler in self.subscribers[topic]:
                try:
                    handler(event)
                except Exception as e:
                    logger.error(f"Error in handler for topic {topic}: {e}")
        return event

    def get_events(self, topic: str = None) -> List[Dict[str, Any]]:
        if topic:
            return [e.to_dict() for e in self.history if e.topic == topic]
        return [e.to_dict() for e in self.history]
