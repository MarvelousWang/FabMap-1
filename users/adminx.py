__author__ = 'Elvan'
__date__ = '2017/8/25 21:52'

import xadmin
from layout.models import EQLayout, Path


class EQLayoutAdmin(object):
    list_display = ['en_name', 'cn_name', 'floor', 'add_time', 'vertex']
    search_fields = ['en_name', 'cn_name', 'floor', 'vertex']
    list_filter = ['en_name', 'cn_name', 'floor', 'add_time', 'vertex']


class PathAdmin(object):
    list_display = ['start_floor', 'start_point', 'end_floor', 'end_point', 'add_time']
    search_fields = ['start_floor', 'start_point', 'end_floor', 'end_point']
    list_filter = ['start_floor', 'start_point', 'end_floor', 'end_point']


xadmin.site.register(EQLayout, EQLayoutAdmin)
xadmin.site.register(Path, PathAdmin)
