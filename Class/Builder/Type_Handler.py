from Class.Interfase.IHandler import AbstractHandler
from Class.Builder.Builder import Director, MainBuilder


class Standarte_Command(AbstractHandler):
    def __init__(self, gen_list):
        self.gen_list = gen_list

    def handle(self, request):
        if request == "StandCommand":
            command = []
            director = Director()
            for i in range(len(self.gen_list)):
                builder = MainBuilder(self.gen_list[i])
                director.builder = builder
                director.standert_command()
                command.append({})
                for data in builder.product.list_parts():
                    command[i][data[0]] = data[1]
            return command
        else:
            return super(Standarte_Command, self).handle(request)


class SortTask(AbstractHandler):

    def __init__(self, gen_list):
        self.gen_list = gen_list

    def handle(self, request):
        if request == "SortTask":
            command = []
            director = Director()
            for i in range(len(self.gen_list)):
                builder = MainBuilder(self.gen_list[i])
                director.builder = builder
                director.sort_task()
                command.append({})
                for data in builder.product.list_parts():
                    command[i][data[0]] = data[1]
            return command
        else:
            return super(SortTask, self).handle(request)
