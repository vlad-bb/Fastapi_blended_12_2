from django.urls import path

from . import views

app_name = 'noteapp'


urlpatterns = [
    path("addtag/", views.AddTag.as_view(), name="addtag"),
    path("addauthor/", views.AddAuthor.as_view(), name="addauthor"),
    path("addquote/", views.AddQuote.as_view(), name="addquote"),
    path("quotes/", views.Quotes.as_view(), name="quotes"),
    path("detail/<int:author_id>", views.AuthorDetail.as_view(), name="detail"),
]
