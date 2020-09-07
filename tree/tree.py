"""Tree structure"""


class Tree:
    """Tree"""

    def __init__(self, value=None):
        self.value = value
        self.left = None
        self.right = None

    def contains(self, value) -> bool:
        """Checks if value is within tree."""
        if self.value == value:
            return True

        if self.value > value:
            try:
                return self.left.contains(value)
            except AttributeError:
                return False

        if self.value < value:
            try:
                return self.right.contains(value)
            except AttributeError:
                return False

        return False

    def add_node(self, value: int) -> None:
        """Add node to tree."""

        if self.value is None:
            self.value = value
        elif self.value < value:
            if self.right is None:
                self.right = Tree(value)
            else:
                self.right.add_node(value)
        elif self.value > value:
            if self.left is None:
                self.left = Tree(value)
            else:
                self.left.add_node(value)

    def __len__(self) -> int:
        if self.value is None:
            return 0

        try:
            left = self.left.__len__()
        except AttributeError:
            left = 0

        try:
            right = self.right.__len__()
        except AttributeError:
            right = 0

        return max(left, right) + 1

    def __to_list(self) -> []:
        if self.left is None and self.right is None:
            return [self.value]

        try:
            left = self.left.__to_list()
        except AttributeError:
            left = None

        try:
            right = self.right.__to_list()
        except AttributeError:
            right = None

        return [left, self.value, right]

    def __repr__(self):
        return str(self.__to_list())
