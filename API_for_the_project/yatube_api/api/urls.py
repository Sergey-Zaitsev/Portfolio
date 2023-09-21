from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework import routers

from api.views import PostViewSet, GroupViewSet, FollowViewSet, CommentViewSet

router_v1 = routers.DefaultRouter()
router_v1.register(r'posts', PostViewSet, basename="Posts")
router_v1.register(r'groups', GroupViewSet, basename="Groups")
router_v1.register(r'follow', FollowViewSet, basename='follow')
router_v1.register(r'posts/(?P<post_id>\d+)/comments',
                   CommentViewSet, basename='Comments')
urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/', include('djoser.urls')),
    path('v1/', include('djoser.urls.jwt')),
    path(
        'redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
]
