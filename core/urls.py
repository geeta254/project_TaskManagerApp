from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # 👇 app URLs connected here
    path('', include('task.urls')),
]