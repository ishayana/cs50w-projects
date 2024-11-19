from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'auctions'

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:listing_id>", views.listing_details, name="listing_details"),
    path("close/<int:listing_id>", views.listing_close, name="listing_close"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("watchlist", views.whatchlist, name="watchlist"),
    path("watchlist/<int:listing_id>", views.add_watchlist, name="add_watchlist"),
    path("category/", views.category, name="category"),
    path("category/<int:category_id>", views.category_details, name="category_details"),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
