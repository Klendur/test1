from django.urls import path
from . import views
from .views import CustomLoginView
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #andmebaas
    path('tooted', views.tootetabel.as_view(), name='tooted'),
    path('upload-toode/', views.upload_excel, name='upload_excel'),
    path('export-excel/', views.export_to_excel, name='export_to_excel'),
    path('toode/<int:pk>/', views.toodedetail.as_view(), name='toode_detail'),
    path('toode/<int:pk>/edit/', views.toodeupdate.as_view(), name='toode_update'),

    path('projektid', views.projektitabel.as_view(), name='projektid'),
    
    path('taskid', views.taskitabel.as_view(), name='taskid'),
    path('view_komplekteeritudkogus/', views.view_komplekteeritudkogus, name='view_komplekteeritudkogus'),




    path('projektivalik', views.projektivalik.as_view(), name='projektivalik'),
    path('projektivaade', views.projektivaadeview, name='projektivaade'),
    path('choose_action/', views.choose_action_view, name='choose_action'),
    path('create_task_form/', views.create_task_form_view, name='create_task_form'),
    path('select_task/', views.task_selection_view, name='task_selection'),
    path('add_products/', views.add_products_to_task_view, name='add_products_to_task'),






    path('', views.pealeht, name='pealeht'),
    path('varvitabelpealeht', views.varvipealeht, name='varvipealeht'),

    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', views.register, name='register'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
]

if settings.DEBUG == False:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)