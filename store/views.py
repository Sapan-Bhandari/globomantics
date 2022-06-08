from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseNotFound
from django.views import View
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.views.generic import TemplateView, ListView


def index(request):
    return HttpResponse("Hello there, e-commerce application store front display")

def detail(request):
    return HttpResponse("Hello there, e-commerce application store front display details")

def logout(request):
    try:
        del request.session['customer']
    except KeyError:
        print("Error while logging out")
    return HttpResponse("You're logged out.")

@csrf_exempt
#@cache_page(900)
@require_http_methods(["GET"])
def electronics(request):

    items = ("Windows PC", "Apple Mac", "Apple iPhone", "Lenovo", "Samsung", "Google")
    if request.method == 'GET':
        paginator = Paginator(items, 2)
        pages = request.GET.get('page', 1)
        name = "Sapan"
        messages.info(request, "Customer successfully fetched")
        try:
            items = paginator.page(pages)
        except PageNotAnInteger:
            items = paginator.page(1)
        if not request.session.has_key('customer'):
            request.session['customer'] = name
            print("Session value set")
        response = render(request, 'store/list.html', {'items': items})
        if request.COOKIES.get('visits'):
            value = int(request.COOKIES.get('visits'))
            print("Getting Cookie.")
            response.set_cookie('visits', value + 1)
        else:
            value = 1
            print("Setting Cookie.")
            response.set_cookie('visits', value)
        return response
        #return render(request, 'store/list.html', {'items': items})
    elif request.method == 'POST':
        return HttpResponseNotFound("Page Not Found")

class ElectronicsView(View):
    def get(self, request):
        items = ("Windows PC", "Apple Mac", "Apple iPhone", "Lenovo", "Samsung", "Google")
        paginator = Paginator(items, 2)
        pages = request.GET.get('page', 1)
        self.process()
        try:
            items = paginator.page(pages)
        except PageNotAnInteger:
            items = paginator.page(1)
        return render(request, 'store/list.html', {'items': items})

    def process(self):
        print("We are processing Electronics")

class ComputersView(ElectronicsView):
    def process(self):
        print("We are processing Computers")

class MobileView():
    def process(self):
        print("We are processing Mobile Phones")

class EquipmentView(MobileView, ComputersView):
    pass

class ElectronicsView2(TemplateView):
    template_name = 'store/list.html'
    def get_context_data(self, **kwargs):
        items = ("Windows PC", "Apple Mac", "Apple iPhone", "Lenovo", "Samsung", "Google")
        context = {'items': items}
        return context

class ElectronicsView3(ListView):
    template_name = 'store/list2.html'
    queryset = ("Windows PC", "Apple Mac", "Apple iPhone", "Lenovo", "Samsung", "Google")
    context_object_name = 'items'
    paginate_by = 2