from django.shortcuts import render
from django.views.generic.base import View
from layout.models import EQLayout, Nodes, AdjMat, Path
from .forms import PathForm
from .minpath import show_paths


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
                mats = AdjMat.objects.all()
                if len(mats) > 0:
                    time_mat = AdjMat.objects.values_list('add_time', flat=True).order_by('-add_time')[0]
                    time_node = Nodes.objects.values_list('add_time', flat=True).order_by('-add_time')[0]
                    if time_node < time_mat:
                        return render(request, "fabmap.html",
                                      {"all_vertex": all_vertex, "msg1": "路径是最新, 不需重新计算."})
                newNode = Nodes.objects.all()
                newMat = self._creat_mat(newnode=newNode)
            return render(request, "fabmap.html", {"all_vertex": all_vertex, "msg1": request.GET.get("purpose") + "完成"})

    @staticmethod
    def _creat_mat(newnode):
        nodelist = newnode.values_list('nodeNo',flat=True)
        inf = float("inf")
        mat = [[inf]*len(nodelist)]*len(nodelist)  # 生成inf组成的初始方阵, 但需注意*是浅拷贝, 所以需要重新拷贝一次
        mat1 = [[mat[i][j] for j in range(len(mat))] for i in range(len(mat))]  # 拷贝mat, 消除浅拷贝
        for i in (range(len(nodelist))):
            mat1[i][i] = 0
        for i in (range(len(nodelist))):
            noderow = newnode[i]
            # for j in (range(len(nodelist))):
            #     nodecol = newnode[j]
            for j in list(noderow.reach_node):
                nodecol = newnode[list(nodelist).index(j)]
                xa = noderow.x_axis
                ya = noderow.y_axis
                xb = nodecol.x_axis
                yb = nodecol.y_axis
                mat1[i][j] = ((xa - xb)**2 + (ya - yb)**2)**0.5
        return mat1

        # for noderecord in newnode:
        #     node_dist = [inf] * len(nodelist)
        #     node_dist[i if nodelist[i] == noderecord.get('nodeNo')] = 0
        #     reach_nodes = noderecord.get('reach_node')
        #     for i in (0, len(nodelist)-1):
                # if nodelist[i] == noderecord.get('nodeNo'):
                #     node_dist[i] = 0
                # node_dist[i if nodelist[i] in reach_nodes] = node_distance(noderecord.get('nodeNo'), nodelist[i])
                # elif nodelist[i] in reach_nodes:
                #     node_dist[i] = noderecord.get('x_axis')
# 2017-9-10 代码写到此


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


