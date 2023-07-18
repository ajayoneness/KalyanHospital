from django import template
from ..models import Patient_LAB
import json



register = template.Library()

@register.simple_tag
def hospital_name():
    return "Kalyan Health Care Pvt. Ltd."

@register.filter()
def to_int(value):
    return int(value)


@register.filter
def lab_values(value, request):
    idd=request.session.get('labid')
    pl = Patient_LAB.objects.get(id=int(idd))
    jsondata = pl.labs
    data = json.loads(jsondata)
    labval=[]
    for j in data['labvalue']:
        labval.append(j)
    result = labval[int(value)]
    return result



@register.filter
def get_session_variable(request, labid):
    idd=request.session.get(labid, 'labid')
    return id



@register.filter(name='range')
def _range(_min, args=None):
    _max, _step = None, None
    if args:
        if not isinstance(args, int):
            _max, _step = map(int, args.split(','))
        else:
            _max = args
    args = filter(None, (_min, _max, _step))
    return range(*args)