from django.urls import path
from . import views

app_name = 'place'

urlpatterns = [
    #####################profile#######################
    path('', view=views.place_list, name='place_list'),
    path('map/', view=views.place_map, name='place_map'),
    path('create/', view=views.place_create, name='place_create'),
    path('detail/<int:pk>/',
         view=views.place_detail, name='place_detail'),
    path('<int:pk>/delete/',
         view=views.place_delete, name='place_delete'),

    # TODO place update시 사진 그대로 가져오기
    path('<int:pk>/update/',
         view=views.place_update, name='place_update'),

]
