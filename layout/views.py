from django.shortcuts import render
from django.views.generic.base import View
from layout.models import EQLayout, Path
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
1. 在xadmin后台更新路径后,重算路径
'''


class FabmapView(View):
    # def allvertex(self):
    #     all_vertex = list(EQLayout.objects.values_list("vertex"))
    #     if all_vertex:
    #         all_vertex = [x[0] for x in all_vertex]
    #         return all_vertex
    #     else:
    #         return False

    def get(self, request):
        all_vertex = list(EQLayout.objects.values_list("vertex"))
        if all_vertex:
            all_vertex = [x[0] for x in all_vertex]
            return render(request, "fabmap.html", {"all_vertex": all_vertex})
        else:
            return render(request, "fabmap.html", {"msg": "还未输入任何设备坐标信息!"})

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
