"""Utilities for aioCloudWeather."""

import asyncio


class LimitedSizeQueue(asyncio.Queue):
    """Queue with limited size that discards oldest items when full."""

    def put_nowait(self, item):
        """Put item without waiting; drop oldest if full."""
        if self.full():
            self.get_nowait()
        super().put_nowait(item)
