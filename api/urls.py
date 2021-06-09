from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'todo', views.ToDoViewSet)
router.register(r'states', views.StatesViewSet)
router.register(r'date', views.DatesViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # path('fill',views.Add_to_database),
    path('cases/<str:date>/<str:state>',views.date_state),
    # path('add',views.Add_to_database),
    # path('delete/',views.delete),
    path('update/',views.update_timeseries)
]