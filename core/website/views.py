from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView,FormView,CreateView
from .forms import PhotoForm
from .models import Photo
# Create your views here.


class UploadView(CreateView):
    template_name = 'website/index.html'
    form_class = PhotoForm
    success_url = '/'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["gallery"] = Photo.objects.all()
        return context
    
    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('file')
        
        if 'file' not in request.FILES or not form.is_valid():
            return HttpResponseRedirect(reverse_lazy("website:index"))
        
        if form.is_valid():
            for file in files:
                Photo.objects.create(file=file)
            return HttpResponseRedirect(self.request.path_info)
        else:
            return self.form_invalid(form)
    
    