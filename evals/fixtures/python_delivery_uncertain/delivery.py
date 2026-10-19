"""Synchronous delivery adapter. The client provides send(key, payload)."""

class TemporaryRejection(Exception):
    """The receiver confirms this attempt was not accepted."""

class DeliveryUncertain(Exception):
    """The outcome needs reconciliation by the caller."""

def deliver(client, key, payload):
    """Return the receiver result. Temporary rejections get at most 3 attempts."""
    for attempt in range(3):
        try:
            return client.send(key, payload)
        except (TemporaryRejection, TimeoutError):
            if attempt == 2:
                raise
