''' Views to run tasks '''
from django.shortcuts import HttpResponse
from .bg_processes.setup_holding_page import setup_dash


def holding_page():
    ''' Returns holding page '''
    dash_config = setup_dash()
    return HttpResponse(f'<div>hello  {dash_config}</div>')
