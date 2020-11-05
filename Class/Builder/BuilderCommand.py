from Class.Builder.Type_Handler import *


def create_command(command, list_main):
    standarta_command = Standarte_Command(list_main)
    sort_task = SortTask(list_main)
    standarta_command.set_next(sort_task)
    result = standarta_command.handle(command)
    return result if result else "None createCommand"
