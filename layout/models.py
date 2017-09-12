from datetime import datetime
from django.db import models


class EQLayout(models.Model):
    en_name = models.CharField(max_length=50, verbose_name="机台名称", default="")
    # cn_name = models.CharField(max_length=50, verbose_name="机台中文名称", default="", null=True, blank=True)
    unit = models.CharField(max_length=50, verbose_name="机台子单元名称", default="", null=True, blank=True)
    floor = models.CharField(choices=(("L20", "L20"), ("L40", "L40")), max_length=10, verbose_name="楼层", default="楼层未选")
    vertex = models.CharField(max_length=500, verbose_name="顶点坐标", null=False, blank=False)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "机台外框图"  # 设置这个类的别名
        verbose_name_plural = verbose_name  # 设置别名的复数形式

    def __str__(self):
        return self.en_name


class Nodes(models.Model):
    nodeNo = models.AutoField(verbose_name="Node Number", primary_key=True)
    floor = models.CharField(choices=(("L20", "L20"), ("L40", "L40")), max_length=10, verbose_name="楼层", default="楼层未选")
    x_axis = models.IntegerField(verbose_name="x axis")
    y_axis = models.IntegerField(verbose_name="y axis")
    reach_node = models.CharField(verbose_name="可达节点", max_length=300)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "节点"
        verbose_name_plural = verbose_name

    # def __str__(self):
    #     return '{0} {1}({2},{3})'.format(self.nodeNo, self.floor, self.x_axis, self.y_axis)


class AdjMat(models.Model):
    mat = models.TextField(verbose_name="Node邻接矩阵")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "邻接矩阵"
        verbose_name_plural = verbose_name


class Path(models.Model):
    # pathNo = models.AutoField(verbose_name="Path Number", primary_key=True)
    start_floor = models.CharField(choices=(("L10", "L10"), ("L20", "L20"), ("L30", "L30"), ("L40", "L40")), max_length=10,
                             verbose_name="起点楼层", default="楼层未选")
    start_point = models.CharField(max_length=10, verbose_name="起点坐标", default="", null=False)
    end_floor = models.CharField(choices=(("L10", "L10"), ("L20", "L20"), ("L30", "L30"), ("L40", "L40")), max_length=10,
                             verbose_name="终点楼层", default="楼层未选")
    end_point = models.CharField(max_length=10, verbose_name="终点坐标", default="", null=False)
    path_node = models.TextField(max_length=2000, verbose_name="路径节点", null=True, blank=True)
    path_axis = models.TextField(max_length=2000, verbose_name="路径节点坐标", null=True, blank=True)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "路径图"  # 设置这个类的别名
        verbose_name_plural = verbose_name  # 设置别名的复数形式

    def __str__(self):
        return '({0})->({1})'.format(self.start_point, self.end_point)
