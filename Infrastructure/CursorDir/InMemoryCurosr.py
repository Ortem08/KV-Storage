from Infrastructure.CursorDir.ICursor import ICursor


class InMemoryCursor(ICursor):
    def __init__(self, index):
        super().__init__('InMemory')

        self.index = index

    def to_json(self) -> str:
        return "InMemoryCursor"

    def is_null(self) -> bool:
        return self.index == -1
