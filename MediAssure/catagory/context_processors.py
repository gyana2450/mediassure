from .models import Catagory

def menu_link(request):
    links=Catagory.objects.all()
    return dict(links=links)
