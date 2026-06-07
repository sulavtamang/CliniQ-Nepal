from django.urls import path
from queues.views import BookTokenView

urlpatterns = [
    path('tokens/book/', BookTokenView.as_view(), name='book-token'),
]