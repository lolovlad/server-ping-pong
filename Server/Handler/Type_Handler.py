import Server.Handler.MainHadler as Hand
import NeuralNet.Traning as neural
import numpy as np
import Server.data_besa.data_mssql as db
import Server.Builder_Command.BuilderCommand as Command #создание команд Command.create_commamd(Type, [])
import Server.Listing as l
import heapq
import json as js
import socket


class NewGoods(Hand.AbstractHandler):
    def gen_sort(self, flag):
        if not flag[0]:
            if flag[2]:
                list_qr = Command.create_command("SortTask", [["Output_avoid_2", ["avoid_2", "output"]]])
                flag = [True, flag[1], False]
                type_1 = 0
            elif flag[1]:
                list_qr = Command.create_command("SortTask", [["Output_avoid_1", ["avoid_1", "output"]]])
                flag = [True, False, flag[2]]
                type_1 = 1
            elif True:
                list_qr = Command.create_command("SortTask", [["Output", ["output", "output"]]])
                flag[0] = True
                type_1 = 2
            return flag, type_1, list_qr
        elif not flag[2]:
            list_qr = Command.create_command("SortTask", [["Input", ["avoid_2"]]])
            flag[2] = True
            return flag, 0, list_qr
        elif not flag[1]:
            list_qr = Command.create_command("SortTask", [["Input", ["avoid_1"]]])
            flag[1] = True
            return flag, 1, list_qr

    def handle(self, request):
        if request["Type_command"] == "New_goods":
            if not l.Lists().list_qr_flag[0] or not l.Lists().list_qr_flag[1] or not l.Lists().list_qr_flag[2]:
                data_base = db.db_sql()
                select = db.db_sql.select_db(data_base, "SELECT * FROM goods_main WHERE name = ?", (request["Goods"]))
                select_info_neural = db.db_sql.select_db(data_base, "SELECT n.* FROM neural_goods_info n INNER JOIN "
                                                                    "goods_main g ON n.id_goods = g.id Where g.name = ?"
                                                         , (request["Goods"]))
                network = neural.NeurlN(learning_rate=0.01, start_weight=1)
                ser = network.predict(np.array(select_info_neural))
                if ser > 0.8:
                    i = 6
                elif ser > 0.65:
                    i = 5
                else:
                    i = 4
                #db.db_sql.select_db(data_base, "SELECT * FROM map_to_day WHERE full_str = 1 and id_graf = ?", (i))
                db.db_sql.update_db(data_base, "UPDATE TOP(1) map_to_day SET id_goods = ? WHERE id_graf = ? "
                                               "WHERE full = 0", (select[0], i))
                select_info = db.db_sql.select_db(data_base, "SELECT m.id_graf, m.side, m.district, m.id FROM "
                                                             "map_to_day m INNER JOIN goods_main g ON m.id_goods = "
                                                             "g.id WHERE g.name = ? and m.full_str = 0",
                                                  (request["Goods"]))
                db.db_sql.update_db(data_base, "UPDATE map_to_day SET full_str = ? WHERE id = ?", (1, select_info[3]))
                select_info = list(select_info)
                select_info.insert(0, "Map")
                com = Command.create_command("StandCommand", [
                    [select_info[0], 1, "Input", "None", select_info[3].replace(' ', '')],
                    [select_info[0], select_info[1], "Input_line", select_info[2].replace(' ', ''), select_info[3].replace(' ', '')]
                ])
                l.Lists().task_list_robot.append(com)
                flag, i, list_qr = self.gen_sort(l.Lists().list_qr_flag)
                l.Lists().list_qr_flag = flag
                heapq.heappush(l.Lists().task_list_sort, (i, list_qr))
                request["sock"].send("ffff".encode())
                return "None"
            else:
                return "None Command"
        else:
            return super(NewGoods, self).handle(request)


class Colibration(Hand.AbstractHandler):
    def handle(self, request):
        if request["Type_command"] == "Colibre":
            try:
                print(request["sock"])
                request["sock"].send(js.dumps(l.Lists().list_cal.pop(0)).encode())
            except IndexError:
                request["sock"].send(js.dumps(Command.create_command("CommandNone", [["Loading", "Loading"]])).encode())
            return "Command sucksesful"
        else:
            return super(Colibration, self).handle(request)


class NewTaskSort(Hand.AbstractHandler):
    def handle(self, request):
        if request["Type_command"] == "New_sort_list":
            try:
                info = js.dumps(heapq.heappop(l.Lists().task_list_sort)[1]).encode()
                request["sock"].send(info)
            except IndexError:
                request["sock"].send(js.dumps(Command.create_command("CommandNone", [["None", "None"]])).encode())
            return "new_sort_list"
        else:
            return super(NewTaskSort, self).handle(request)


class NewTaskRobot(Hand.AbstractHandler):
    def handle(self, request):
        if request["Type_command"] == "List_work+":
            i = -1
            l.Lists().robot_state[request["District"]] = request["Task"]
            for o in l.Lists().task_list_robot:
                if o[1]["District"] == request["District"]:
                    i = l.Lists().task_list_robot.index(o)
                    break
            if i == -1:
                ts = js.dumps(Command.create_command("CommandNone", [["None", "None"]])).encode()
            else:
                ts = js.dumps(l.Lists().task_list_robot.pop(i)).encode()
                i = -1
            request["sock"].send(ts)
            return "list_work+"
        else:
            return super(NewTaskRobot, self).handle(request)


class RefreshState(Hand.AbstractHandler):
    def handle(self, request):
        if request["Type_command"] == "Refresh_state":
            l.Lists().robot_state[request["District"]] = request["Task"]
            request["sock"].send("gg".encode())
            return "refresh_state"
        else:
            return super(RefreshState, self).handle(request)


class InfoTime(Hand.AbstractHandler):

    def time(self, info):
        if info == "Input":
            __tp = 10
        elif info == "Output":
            __tp = 0
        else:
            __tp = 1
        return __tp

    def handle(self, request):
        if request["Type_command"] == "Time":
            if request["District"] == "A":
                g = "B"
            else:
                g = "A"
            ts = str(self.time(l.Lists().robot_state[g])).encode()
            request["sock"].send(ts)
            return "time"
        else:
            return super(InfoTime, self).handle(request)


class NewAngle(Hand.AbstractHandler):
    def calibration(self, data):
        col = data["Info"]
        col.pop("robot")
        for i in col:
            col[i].pop("Rect")
            col[i].pop("Flag")
        map = Command.create_command("AngleTask", [["Col", col]])
        return map

    def handle(self, request):
        if request["Type_command"] == "Angle":
            l.Lists().list_cal.append(self.calibration(request))
            return "angel"
        else:
            return super(NewAngle, self).handle(request)


class RefreshFlag(Hand.AbstractHandler):

    def gen_sort(self, flag, ty):
        if not flag[0]:
            if flag[2]:
                list_qr = Command.create_command("SortTask", [["Output_avoid_2", ["avoid_2", "output"]]])
                flag = [True, flag[1], False]
                type_1 = 0
                return flag, type_1, list_qr
            elif flag[1]:
                list_qr = Command.create_command("SortTask", [["Output_avoid_1", ["avoid_1", "output"]]])
                flag = [True, False, flag[2]]
                type_1 = 1
                return flag, type_1, list_qr
            elif ty:
                list_qr = Command.create_command("SortTask", [["Output", ["output", "output"]]])
                flag[0] = True
                type_1 = 2
                return flag, type_1, list_qr
            elif not ty:
                return flag, "None", "None"
        elif not flag[2]:
            list_qr = Command.create_command("SortTask", [["Input", ["avoid_2"]]])
            flag[2] = True
            return flag, 0, list_qr
        elif not flag[1]:
            list_qr = Command.create_command("SortTask", [["Input", ["avoid_1"]]])
            flag[1] = True
            return flag, 1, list_qr

    def handle(self, request):
        if request["Type_command"] == "Refresh_flag":
            l.Lists().list_qr_flag[0] = False
            lisq_qr_flag, type_1, list_qr = self.gen_sort(l.Lists().list_qr_flag, False)
            if not list_qr == "None":
                heapq.heappush(l.Lists().task_list_sort, (type_1, list_qr))
            return "refresh_flag"
        else:
            return super(RefreshFlag, self).handle(request)


class User(Hand.AbstractHandler):
    def handle(self, request):
        if request["Type_command"] == "Our_cube":
            data_base = db.db_sql()
            select_id = db.db_sql.select_db(data_base, "SELECT id FROM goods_main WHERE name = ? SET ROWCOUNT 1", (request["Goods"]))
            select = db.db_sql.select_db(data_base, "SELECT id_graf, side, district FROM map_to_day WHERE id_goods = ? and full_str=1",
                                         select_id[0])
            db.db_sql.update_db(data_base, "UPDATE map_to_day SET full_str=0 WHERE id_goods = ? and full_str=1",
                                (select_id[0]))
            com = Command.create_command("StandCommand", [
                ["Map", select[0], "Output_line", select[1].replace(' ', ''), select[2].replace(' ', '')],
                ["Map", 7, "Output", "None", select[2].replace(' ', '')]
            ])
            l.Lists().task_list_robot.append(com)
            return "our_cube"
        else:
            return super(User, self).handle(request)
