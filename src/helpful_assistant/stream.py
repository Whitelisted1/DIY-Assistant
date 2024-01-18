from typing import Generator, Callable


class Stream:
    def __init__(self, generator: Generator, callback: Callable) -> None:
        self.generator = generator
        self.callback = callback

    def __iter__(self):
        out = []
        for item in self.generator:
            out.append(item)
            yield item

        self.callback(out)
