from django.urls import path

from .import views

urlpatterns = [
    # /j24_t1/    
    path('',views.index,name='index'),
    # /j24_t1/5/
    path('<int:question_id>/',views.detail,name='detail'),
    # /j24_t1/5/results/
    path('<int:question_id>/results/',views.results,name='results'),
    # /j24_t1/5/vote/
    path('<int:question_id>/vote/',views.vote,name='vote'),
]

