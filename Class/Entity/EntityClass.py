import pyodbc
from Class.Interfase.Fluent import Fluent
from Class.Interfase.IModel import IModel


class EntityModel(Fluent.Fluent):
    def __init__(self, model_info, db, link):
        self.__model_info = model_info
        self.__list_model = []
        self.__content = db
        self.__link = link
        self.__hash_table = None
        self.__list_save = []

    def load(self):
        self.__content.execute("Select * From " + self.__model_info.name_model() + "")
        result = self.__content.fetchall()
        self.__link.commit()
        for i in result:
            self.__list_model.append(self.__model_info(i))

    def where(self, lmd):
        self.__hash_table = list(filter(lmd, self.__list_model))

    def first_of_default(self):
        return self.__hash_table[0]

    def delite(self, model=None):
        if isinstance(model, IModel):
            self.__list_save.append((model, "delite"))
        elif model is None:
            for i in self.__hash_table:
                self.__list_save.append((i, "delite"))
        else:
            for i in list(filter(model, self.__list_model)):
                self.__list_save.append((i, "delite"))

    def add(self, model):
        self.__list_save.append((model, "add"))

    def update(self, model):
        if isinstance(model, IModel):
            self.__list_save.append((model, "update"))

    def save_change(self):
        cl_name = self.__column_name()
        for i in self.__list_save:
            if i[1] == "delite":
                sql = "DELETE FROM " + self.__model_info.name_model() + " WHERE  Id = ?"
                self.__content.execute(sql, (i[0].id, ))
                self.__link.commit()
            elif i[1] == "add":
                str_cl_name = ", ".join(cl_name[1:],)
                value = ""
                for k in range(len(i[0].get_list_interfase()[1:])):
                    value += "?, "
                sql = "INSERT INTO " + self.__model_info.name_model() + "(" + str_cl_name + ") VALUES " \
                      + "(" + value[:len(value) - 2] + ")"
                self.__content.execute(sql, tuple(i[0].get_list_interfase()[1:]))
                self.__link.commit()
                print(sql, i[0].get_list_interfase()[1:])
            elif i[1] == "update":
                value = ""
                for k in range(1, len(i[0].get_list_interfase())):
                    value += cl_name[k] + " = ?, "
                print(value)
                sql = "UPDATE " + self.__model_info.name_model() + " SET " + value[:len(value) - 2] + \
                      " WHERE Id = ?"
                args = i[0].get_list_interfase()[1:] + [i[0].get_list_interfase()[0]]
                self.__content.execute(sql, tuple(args))
                self.__link.commit()

    def list_model(self):
        return self.__list_model

    def get_name(self):
        return self.__model_info.nm()

    def __column_name(self):
        self.__content.execute("EXEC sp_columns " + self.__model_info.name_model())
        result = list(map(lambda x: x[3], self.__content.fetchall()))
        return result


