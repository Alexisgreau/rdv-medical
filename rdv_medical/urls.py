from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView, LoginView
from django.urls import reverse_lazy

class LogoutGetView(LogoutView):
    http_method_names = ['get', 'post']

urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/login/",
         LoginView.as_view(template_name="registration/login.html"),
         name="login"),
    path('', include('app.urls')),
    path(
        'accounts/logout/',
        LogoutGetView.as_view(next_page=reverse_lazy('home')),
        name='logout'
    ),
]
