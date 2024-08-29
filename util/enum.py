"""
Copyright (c) 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010,
2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023 Python Software Foundation;
All Rights Reserved

- Note
Inspired by the EnumMeta metaclass in the python standard library.
Similarities in approach can be found in the `__new__` method.
"""

"""
Copyright (c) 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010,
2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023 Python Software Foundation;
All Rights Reserved
"""


class DynamicClassAttribute:
    """Route attribute access on a class to __getattr__.

    This is a descriptor, used to define attributes that act differently when
    accessed through an instance and through a class.  Instance access remains
    normal, but access to an attribute through a class will be routed to the
    class's __getattr__ method; this is done by raising AttributeError.

    This allows one to have properties active on an instance, and have virtual
    attributes on the class with the same name (see Enum for an example).

    """

    def __init__(self, fget=None, fset=None, fdel=None, doc=None):
        self.fget = fget
        self.fset = fset
        self.fdel = fdel
        # next two lines make DynamicClassAttribute act the same as property
        self.__doc__ = doc or fget.__doc__
        self.overwrite_doc = doc is None
        # support for abstract methods
        self.__isabstractmethod__ = bool(getattr(fget, "__isabstractmethod__", False))

    def __get__(self, instance, ownerclass=None):
        if instance is None:
            if self.__isabstractmethod__:
                return self
            raise AttributeError()
        if self.fget is None:
            raise AttributeError("unreadable attribute")
        return self.fget(instance)

    def __set__(self, instance, value):
        if self.fset is None:
            raise AttributeError("can't set attribute")
        self.fset(instance, value)

    def __delete__(self, instance):
        if self.fdel is None:
            raise AttributeError("can't delete attribute")
        self.fdel(instance)

    def getter(self, fget):
        fdoc = fget.__doc__ if self.overwrite_doc else None
        result = type(self)(fget, self.fset, self.fdel, fdoc or self.__doc__)
        result.overwrite_doc = self.overwrite_doc
        return result

    def setter(self, fset):
        result = type(self)(self.fget, fset, self.fdel, self.__doc__)
        result.overwrite_doc = self.overwrite_doc
        return result

    def deleter(self, fdel):
        result = type(self)(self.fget, self.fset, fdel, self.__doc__)
        result.overwrite_doc = self.overwrite_doc
        return result


class EnumItem:
    def __init__(self, enum_class_name, name, value):
        self.enum_class_name = enum_class_name
        self._name_ = name
        self._value_ = value

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.value == other.value
        if isinstance(other, type(self.value)):
            return self.value == other
        return False

    def __lt__(self, other):
        if isinstance(other, type(self)):
            return self.value < other.value
        if isinstance(other, type(self.value)):
            return self.value < other
        return False

    def __gt__(self, other):
        if isinstance(other, type(self)):
            return self.value > other.value
        if isinstance(other, type(self.value)):
            return self.value > other
        return False

    def __le__(self, other):
        return not (self > other)

    def __ge__(self, other):
        return not (self < other)

    def __and__(self, other):
        if isinstance(other, type(self)):
            return self.value & other.value
        return self.value & other

    def __or__(self, other):
        if isinstance(other, type(self)):
            return self.value | other.value
        return self.value | other

    def __xor__(self, other):
        if isinstance(other, type(self)):
            return self.value ^ other.value
        return self.value ^ other

    def __int__(self):
        return int(self.value)

    def __float__(self):
        return float(self.value)

    def __str__(self):
        return str(self.value)

    def __hash__(self):
        return hash(self._name_)

    def __repr__(self):
        return f"<{self.enum_class_name}.{self.name}: '{self}'>"

    @DynamicClassAttribute
    def name(self):
        """The name of the Enum member."""
        return self._name_

    @DynamicClassAttribute
    def value(self):
        """The value of the Enum member."""
        return self._value_

class EnumMetaClass(type):
    def __new__(mcs, name, bases, attributes):
        # Extracts the non dunder methods from attributes list in order
        # to create the enum items
        enum_map = {}
        for attribute_name, attribute_value in attributes.items():
            if not attribute_name.startswith("__"):
                enum_map[attribute_name] = attribute_value

        for attribute_name in enum_map.keys():
            attributes.pop(attribute_name)

        # Creates derived enum class
        enum_class = super().__new__(mcs, name, bases, attributes)

        class EnumClassItem(EnumItem):
            pass

        enum_class.Item = EnumClassItem

        enum_item_map = {}

        # Adds enum items to derived enum class
        for attribute_name, attribute_value in enum_map.items():
            enum_item = enum_class.Item(mcs, attribute_name, attribute_value)
            setattr(enum_class, attribute_name, enum_item)
            enum_item_map[attribute_name] = enum_item

        enum_class.enum_item_map = enum_item_map

        return enum_class

    def __str__(cls):
        return f"<enum '{cls.__name__}'>"

    def __iter__(self):
        self.enum_map_iter = iter(getattr(self, "enum_item_map", {}).values())
        return self.enum_map_iter

    def __next__(self):
        self.enum_map_iter = next(self.enum_map_iter)
        return self.enum_map_iter


class Enum(metaclass=EnumMetaClass):
    def __str__(self):
        return f"{self.__class__.__name__}.{self._name_}"

    @classmethod
    def item(cls):
        return

    def __new__(cls, value):
        for enum_item in cls:
            if value == enum_item.value:
                return enum_item
        return None
