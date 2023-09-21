from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import IngredientViewSet, RecipeViewSet, TagViewSet, UserViewSet

router_v1 = DefaultRouter()

router_v1.register("ingredients", IngredientViewSet,
                   "ingredients")
router_v1.register("recipes", RecipeViewSet, "recipes")
router_v1.register("tags", TagViewSet, "tags")
router_v1.register("users", UserViewSet, "users")

urlpatterns = [
    path('', include(router_v1.urls)),
    path("api/", include(router_v1.urls)),
    path("api/auth/", include("djoser.urls.authtoken")),
    path("admin/", admin.site.urls),
]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL,
#                           document_root=settings.MEDIA_ROOT)
