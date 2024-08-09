from django.urls import path
from app.routes.insert import insert
from app.routes.find import find
from app.routes.delete import delete
from app.routes.update import update

urlpatterns = [
    path('insert/', insert),
    path('find/', find),
    path('delete/', delete),
    path('update/', update)
]