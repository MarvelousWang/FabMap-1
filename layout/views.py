from django.shortcuts import render
from django.views.generic.base import View
from layout.models import EQLayout, Nodes, AdjMat, Path
from .forms import PathForm
from .minpath import GraphAL, floyd_paths, show_paths


'''
数据库获取路径的过程:
1. 浏览器输入起点和终点, 返回服务器
2. 服务器在path数据库中查询起点和终点, 将路径返回给浏览器
3. 浏览器在页面上画出路径

即时计算路径的过程:
1. 浏览器输入起点和终点, 返回服务器
2. 服务器从数据库获取路径graph, 再即时计算路径, 并将路径返回浏览器
3. 浏览器在页面上画出路径

更新设备外框图和路径图
1. 在xadmin后台更新路径, 或者数据库导入路径
2. 在页面上按重新计算路径, 服务器比对node版本与path的版本, 若path版本较旧, 则重新计算path.
'''


class FabmapView(View):
    def get(self, request):
        all_vertex = list(EQLayout.objects.values_list("vertex", flat=True))
        # all_vertex = [x[0] for x in all_vertex]
        if not request.GET.get("purpose"):
            return render(request, "fabmap.html", {"all_vertex": all_vertex})
        else:
            if request.GET.get("purpose") == "重算路径":
                paths = Path.objects.all()
                if len(paths) > 0:
                    time_path = Path.objects.values_list('add_time', flat=True).order_by('-add_time')[0]
                    time_node = Nodes.objects.values_list('add_time', flat=True).order_by('-add_time')[0]
                    if time_node < time_path:
                        return render(request, "fabmap.html",
                                      {"all_vertex": all_vertex, "msg1": "路径是最新, 不需重新计算."})
                newNode = Nodes.objects.all()
                nodelist = list(newNode.values_list('nodeNo', flat=True))
                newMat = self._creat_mat(newnode=newNode)
                new_mat = AdjMat()
                new_mat.mat = newMat
                new_mat.save()  # 将新的邻接矩阵保存到数据库中
                graph = GraphAL(newMat)  # 实例化graph
                pathstack = floyd_paths(graph)  # 计算出所有顶点间路径
                for start_node in newNode:
                    for end_node in newNode:
                        new_path = Path()
                        new_path.start_floor = start_node.floor
                        new_path.start_point = '{0},{1}'.format(start_node.x_axis, start_node.y_axis)
                        new_path.end_floor = end_node.floor
                        new_path.end_point = '{0},{1}'.format(end_node.x_axis, end_node.y_axis)
                        temp1 = start_node.nodeNo
                        temp2 = end_node.nodeNo
                        temp10 = nodelist.index(temp1)
                        temp20 = nodelist.index(temp2)
                        path_node = show_paths(pathstack, temp10, temp20)[0]  # 该路径只是节点名称的序列, 不是节点坐标序列
                        path_node = [nodelist[path_node[i]] for i in range(len(path_node))]
                        new_path.path_node = path_node
                        path_node_axis = ["{0},{1}".format(newNode.get(nodeNo=nodeNo).x_axis, newNode.get(nodeNo=nodeNo).y_axis) for nodeNo in path_node]
                        new_path.path_axis = " ".join(path_node_axis)
                        new_path.save()
            return render(request, "fabmap.html", {"all_vertex": all_vertex, "msg1": request.GET.get("purpose") + "完成"})

    @staticmethod
    def _creat_mat(newnode):
        nodelist = newnode.values_list('nodeNo', flat=True)
        inf = float("inf")
        mat = [[inf for col in range(len(nodelist))] for row in range(len(nodelist))]
        for i in (range(len(nodelist))):
            mat[i][i] = 0  # 将对角线元素置零
        for i in (range(len(nodelist))):
            noderow = newnode[i]  # 逐个取出元素作为行元素
            temp = noderow.reach_node
            temp1 = temp.split(',')  # 将字符转换为列表
            for j in temp1:
                j = int(j)  # j原来是str, 不能作为列表索引,需转换为数字
                temp2 = list(nodelist)
                temp3 = temp2.index(j)
                nodecol = newnode[temp3]
                xa = noderow.x_axis
                ya = noderow.y_axis
                xb = nodecol.x_axis
                yb = nodecol.y_axis
                mat[i][temp3] = round(((xa - xb)**2 + (ya - yb)**2)**0.5, 3)
        return mat

    def post(self, request):
        path_form = PathForm(request.POST)
        if path_form.is_valid():  # 检查login_form是否出错, 没出错的才验证用户名和密码
            start_floor = request.POST.get("start_floor", "")
            start_point = request.POST.get("start_point", "")
            end_floor = request.POST.get("end_floor", "")
            end_point = request.POST.get("end_point", "")
            path = Path.objects.get(
                start_floor=start_floor,
                start_point=start_point,
                end_floor=end_floor,
                end_point=end_point)
            if path:
                all_vertex = list(EQLayout.objects.values_list("vertex", flat=True))
                return render(request, "fabmap.html", {"all_vertex": all_vertex, "path_node": path.path_node})
            else:
                return render(request, "fabmap.html", {"msg": "路径尚未生成!"})
        else:
            return render(request, "fabmap.html", {"msg": "请输入坐标"})


class L40View(View):
    def get(self, request):
        all_vertex = list(EQLayout.objects.values_list("vertex"))
        if all_vertex:
            all_vertex = [x[0] for x in all_vertex]
            return render(request, "L40.html", {"all_vertex": all_vertex})
        else:
            return render(request, "L40.html", {"msg": "还未输入任何设备坐标信息!"})

    def post(self, request):
        path_form = PathForm(request.POST)
        if path_form.is_valid():  # 检查login_form是否出错, 没出错的才验证用户名和密码
            start_floor = request.POST.get("start_floor", "")
            start_point = request.POST.get("start_point", "")
            end_floor = request.POST.get("end_floor", "")
            end_point = request.POST.get("end_point", "")
            path = Path.objects.get(
                start_floor=start_floor,
                start_point=start_point,
                end_floor=end_floor,
                end_point=end_point)
            if path:
                all_vertex = list(EQLayout.objects.values_list("vertex"))
                if all_vertex:
                    all_vertex = [x[0] for x in all_vertex]
                return render(request, "L40.html", {"all_vertex": all_vertex, "path_node": path.path_node})
            else:
                return render(request, "L40.html", {"msg": "路径尚未生成!"})
        else:
            return render(request, "L40.html", {"msg": "请输入坐标"})


class L20View(View):
    def get(self, request):
        all_vertex = list(EQLayout.objects.values_list("vertex"))
        if all_vertex:
            all_vertex = [x[0] for x in all_vertex]
            return render(request, "L20.html", {"all_vertex": all_vertex})
        else:
            return render(request, "L20.html", {"msg": "还未输入任何设备坐标信息!"})

    def post(self, request):
        path_form = PathForm(request.POST)
        if path_form.is_valid():  # 检查login_form是否出错, 没出错的才验证用户名和密码
            start_floor = request.POST.get("start_floor", "")
            start_point = request.POST.get("start_point", "")
            end_floor = request.POST.get("end_floor", "")
            end_point = request.POST.get("end_point", "")
            path = Path.objects.get(
                start_floor=start_floor,
                start_point=start_point,
                end_floor=end_floor,
                end_point=end_point)
            if path:
                all_vertex = list(EQLayout.objects.values_list("vertex"))
                if all_vertex:
                    all_vertex = [x[0] for x in all_vertex]
                return render(request, "L20.html", {"all_vertex": all_vertex, "path_node": path.path_node})
            else:
                return render(request, "L20.html", {"msg": "路径尚未生成!"})
        else:
            return render(request, "L20.html", {"msg": "请输入坐标"})


