# tribes/urls.py
from django.urls import path
from .views import PeopleListView, PeopleDetailView, UserRegistrationView, ChatView, FavoriteListView, FavoriteDeleteView, CommentListView, UserProfileView, ChangePasswordView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('api/tribes/', PeopleListView.as_view(), name='tribes-list'),
    path('api/tribes/<slug:slug>/', PeopleDetailView.as_view(), name='tribes-detail'),
    path('api/tribes/<slug:slug>/chat/', ChatView.as_view(), name='chat'),
    path('api/tribes/<slug:slug>/comments/', CommentListView.as_view(), name='comments-list'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/', UserRegistrationView.as_view(), name='register'),
    path('api/chat/<slug:slug>/', ChatView.as_view(), name='chat'),
    path('api/favorites/', FavoriteListView.as_view(), name='favorites-list'),
    path('api/favorites/<int:pk>/', FavoriteDeleteView.as_view(), name='favorites-delete'),
    path('api/profile/', UserProfileView.as_view(), name='user-profile'),
    path('api/change-password/', ChangePasswordView.as_view(), name='change-password'),
]