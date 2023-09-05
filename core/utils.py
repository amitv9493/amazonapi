from django.http import HttpRequest

def save_data_to_session(request:HttpRequest, **kwargs):
    for key, value in kwargs.items():
        request.session[key] = value
        request.session.modified = True
        