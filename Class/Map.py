from pygame.sprite import RenderPlain
from pygame import Surface, sprite, Rect
from Model.Border import Border
from Model.Energy import Energy


class Map:
    def __init__(self, color_border, position_borders, size_borders, color_energy, position_energy, size_energy):
        self.__color_border = color_border
        self.__borders = []
        self.__borders_render = []
        self.__position_border = position_borders
        self.__size_borders = size_borders

        self.__color_energy = color_energy
        self.__energys = []
        self.__energys_render = []
        self.__position_energy = position_energy
        self.__size_energy = size_energy

        self.create_border()
        self.create_energy()

    def create_border(self):
        for i, z in zip(self.__position_border, self.__size_borders):
            border = Border(i, z, self.__color_border)
            self.__borders.append(border.rect)
            self.__borders_render.append(border)

    def create_energy(self):
        info = 1
        for i, z in zip(self.__position_energy, self.__size_energy):
            energy = Energy(i, z, self.__color_energy, info, 33)
            info += 1
            self.__energys.append(energy.rect)
            self.__energys_render.append(energy)

    def get_borders_render(self):
        return self.__borders_render

    def get_borders(self):
        return self.__borders

    def get_energy_render(self):
        return self.__energys_render

    def get_energy(self):
        return self.__energys
