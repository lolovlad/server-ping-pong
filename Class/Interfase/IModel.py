from abc import ABC, abstractmethod


class IModel(ABC):
    @abstractmethod
    def get_list_interfase(self):
        return ""

    @abstractmethod
    def __str__(self):
        return ""

    @abstractmethod
    def __repr__(self):
        return ""

    @abstractmethod
    def __deepcopy__(self):
        pass

    @abstractmethod
    def name_model(self):
        pass

    @abstractmethod
    def __call__(self, args, **kwargs):
        pass

