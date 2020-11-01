from django.urls import path
from . import views
# この 「.」は同じ階層(同じフォルダ内)のという意味

app_name = 'blog_app'
urlpatterns = [
   path('', views.index, name='index'),
   path('detail/<int:post_id>/', views.detail, name='detail'),
   # このnameは、templateのindex.html内の{% XXX 'blog_app:detail_XXX' XXX=XXX %} に対応している
   path('add/', views.add, name='add'),
   path('edit/<int:post_id>/', views.edit, name='edit'),
   path('delete/<int:post_id>/', views.delete, name='delete'),
   path('contact/', views.contact, name='contact'),
   path('contact/done/', views.done, name='done'),
   path('like/', views.like, name='like'),
   path('comment/<int:comment_id>/', views.comment_delete, name='comment_delete'),
]