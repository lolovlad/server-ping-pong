from abc import ABC, abstractmethod, abstractproperty


class Builder(ABC):

    @abstractproperty
    def product(self):
        pass

    @abstractmethod
    def type_command(self):
        pass

    @abstractmethod
    def indeks(self):
        pass

    @abstractmethod
    def type_line(self):
        pass

    @abstractmethod
    def side(self):
        pass

    @abstractmethod
    def district(self):
        pass

    @abstractmethod
    def list(self):
        pass

    @abstractmethod
    def angle(self):
        pass
