from django.shortcuts import redirect
from django.views.generic import TemplateView, CreateView
from .tasks import complete_order
from .models import Order
from datetime import datetime

class IndexView(TemplateView):
    template_name = "board/index.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders'] = Order.objects.all()
        return context
    
class NewOrderView(CreateView):
    model = Order
    fields = ['products']
    template_name = 'board/new.html'
    
    def form_valid(self, form):
        order = form.save()
        order.cost = sum([prod.price for prod in order.products.all()])
        order.save()
        complete_order.apply_async([order.pk], countdown = 5)
        return redirect('/')
        

def take_order(request, oid):
    order = Order.objects.get(pk=oid)
    order.time_out = datetime.now()
    order.save()
    return redirect('/')
    
