from collections.abc import MutableSequence

from .item import ItemStack


class Inventory(MutableSequence):
    """A list-like object that represents a minecraft inventory."""

    _inventory: "list[ItemStack]"

    def __init__(self, capacity: int) -> None:
        self._inventory = [None] * capacity

    def __delitem__(self, i: int) -> None:
        self._inventory[i] = None

    def __getitem__(self, i: "int | slice") -> "ItemStack | list[ItemStack]":
        return self._inventory[i]

    def __setitem__(self, i: int, item_stack: ItemStack) -> None:
        if item_stack is not None and type(item_stack) is not ItemStack:
            raise TypeError(
                f"Inventory can only hold ItemStack objects or None. Supplied: {type(input)}"
            )
        self._inventory[i] = item_stack

    def __iter__(self) -> iter:
        yield from self._inventory

    def __contains__(self, item) -> bool:
        return item in self._inventory

    def __len__(self) -> int:
        return len(self._inventory)

    def __copy__(self) -> "Inventory":
        inst = self.__class__.__new__(self.__class__)
        inst.__dict__.update(self.__dict__)
        # Create a copy and avoid triggering descriptors
        inst.__dict__["_inventory"] = self.__dict__["_inventory"][:]
        return inst

    def set_slot(self, slot: int, item_stack: ItemStack) -> None:
        """Set item stack for desired slot."""
        self.__setitem__(slot, item_stack)

    def get_slot(self, slot: int) -> ItemStack:
        """Get item stack in desired slot."""
        return self.__getitem__(slot)

    def pop(self, slot: int = None) -> ItemStack:
        """Remove and return item stack at slot. If no slot specified, get last non-empty slot.

        Raises IndexError if inventory is empty.
        Raises IndexError if slot does not contain item.
        """
        if slot is None:
            slot = next(
                (
                    len(self._inventory) - 1 - s
                    for s, item in enumerate(self._inventory[::-1])
                    if item is not None
                ),
                None,
            )
        if slot is None:
            raise IndexError("pop from empty inventory")

        item_stack = self.get_slot(slot)
        if item_stack is None:
            raise IndexError("pop from empty slot")

        self.__delitem__(slot)
        return item_stack

    def remove(self, item_stack: ItemStack) -> None:
        """Search for and remove the first equivalent item_stack in inventory."""
        slot = next(
            (slot for slot, item in enumerate(self._inventory) if item == item_stack),
            None,
        )
        if slot is not None:
            self.__delitem__(slot)

    def clear(self) -> None:
        """Remove all items from every slot in inventory."""
        self._inventory = [None for _ in self._inventory]

    def copy(self) -> "Inventory":
        """Make a shallow copy of the inventory."""
        return Inventory.create_from_list(self._inventory)

    def count(self, item_stack: ItemStack) -> int:
        """Return number of occurrences of value."""
        return self._inventory.count(item_stack)

    def index(self, item_stack, *args) -> int:
        """Return slot of first matching item stack.

        Raises ValueError if the value is not present.
        """
        return self._inventory.index(item_stack, *args)

    def reverse(self) -> None:
        """Reverses the order of all slots in inventory."""
        self._inventory.reverse()

    def sort(self, /, *args, **kwds) -> None:
        """Sort the inventory according to built-in python list sort."""
        self._inventory.sort(*args, **kwds)

    def insert(self, *args) -> None:
        raise NotImplementedError

    @staticmethod
    def create_from_list(items: "list[ItemStack]") -> "Inventory":
        inv = Inventory(len(items))
        for slot, item_stack in enumerate(items):
            inv.set_slot(slot, item_stack)
        return inv
