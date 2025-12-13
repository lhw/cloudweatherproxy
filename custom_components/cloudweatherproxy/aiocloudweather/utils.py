import asyncio


class LimitedSizeQueue(asyncio.Queue):
    def put_nowait(self, item):
        if self.full():
            self.get_nowait()
        super().put_nowait(item)
