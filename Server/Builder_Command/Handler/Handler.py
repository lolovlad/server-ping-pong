import Server.Builder_Command.Handler.Type_Handler as Type

def code(command, list_main):

    CommandNone = Type.Command_None(list_main)
    StandartaCommand = Type.Standarte_Command(list_main)
    SortTask = Type.SortTask(list_main)
    AngleTask = Type.AngleTask(list_main)

    CommandNone.set_next(StandartaCommand).set_next(SortTask).set_next(AngleTask)
    result = CommandNone.handle(command)
    return result if result else "None createCommand"
