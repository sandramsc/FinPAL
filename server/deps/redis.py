import os
from typing import Generator
from redis import Redis
from dotenv import load_dotenv
from typings.index import MessageEvent

load_dotenv()

r: Redis = Redis.from_url(os.getenv("REDIS_URL"))


class PubSub:
    def __init__(self, key=str) -> None:
        self.key = key

    def publish(self, event: MessageEvent) -> int:
        print("publish", event)
        return r.publish(self.key, event.model_dump_json())

    def subscribe(self) -> Generator[str, None, None]:
        pubsub = r.pubsub()
        pubsub.subscribe(self.key)
        for event in pubsub.listen():
            if event["type"] == "message":
                print("subscribe-event", event)
                yield event["data"]


class Cache:
    def __init__(self) -> None:
        pass

    def set(self, key: str, value: str) -> str:
        r.set(key, value)
        return value

    def get(self, key: str) -> str:
        res = r.get(key)
        return res
