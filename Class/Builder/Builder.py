from Class.Interfase.IBuilder import Builder


class MainBuilder(Builder):
    def __init__(self, list_val):
        self.reset()
        self.value = list_val
        self.__product = None

    def reset(self):
        self.__product = Command()

    @property
    def product(self):
        product = self.__product
        self.reset()
        return product

    def type_command(self):
        self.__product.add(["Type", self.value[0]])

    def indeks(self):
        self.__product.add(["Indeks", self.value[1]])

    def type_line(self):
        self.__product.add(["Type_line", self.value[2]])

    def side(self):
        self.__product.add(["Side", self.value[3]])

    def district(self):
        self.__product.add(["District", self.value[4]])

    def list(self):
        self.__product.add(["List", self.value[1]])

    def angle(self):
        self.__product.add(["Angel", self.value[1]])


class Command:
    def __init__(self):
        self.parts = []

    def add(self, part):
        self.parts.append(part)

    def list_parts(self):
        return self.parts


class Director:
    def __init__(self):
        self.__builder = None

    @property
    def builder(self):
        return self.__builder

    @builder.setter
    def builder(self, builder):
        self.__builder = builder

    def standert_command(self):
        self.builder.type_command()
        self.builder.indeks()
        self.builder.type_line()
        self.builder.side()
        self.builder.district()

    def sort_task(self):
        self.builder.type_command()
        self.builder.indeks()
