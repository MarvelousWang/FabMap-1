from django import forms


class PathForm(forms.Form):
    start_floor = forms.CharField(required=True)
    start_point = forms.CharField(required=True)  # 待增加正则表达式验证坐标格式
    end_floor = forms.CharField(required=True)
    end_point = forms.CharField(required=True)
