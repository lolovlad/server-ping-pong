import Server.Handler.Type_Handler as Type

New_goods = Type.NewGoods()
Colibrated = Type.Colibration()
New_Task_Sort = Type.NewTaskSort()
New_Task_Robot = Type.NewTaskRobot()
Refresh_state = Type.RefreshState()
Info_Time = Type.InfoTime()
New_Angle = Type.NewAngle()
Refresh_Flag = Type.RefreshFlag()
User = Type.User()

New_goods.set_next(Colibrated).set_next(New_Task_Sort).set_next(New_Task_Robot).set_next(Refresh_state).set_next(Info_Time).set_next(New_Angle).set_next(Refresh_Flag).set_next(User)

def task(command):
    result = New_goods.handle(command)
    return result if result else "None command"
