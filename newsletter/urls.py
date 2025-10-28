from functools import cache

from django.urls import path

from django.views.decorators.cache import cache_page

from newsletter.apps import NewsletterConfig
from newsletter.views import (
    ClientListView,
    ClientDetailView,
    ClientCreateView,
    ClientUpdateView,
    ClientDeleteView,
    MessagesListView,
    MessagesDetailView,
    MessagesCreateView,
    MessagesUpdateView,
    MessagesDeleteView,
    MailingsListView,
    MailingsDetailView,
    MailingsCreateView,
    MailingsUpdateView,
    MailingsDeleteView,
)

app_name = NewsletterConfig.name

urlpatterns = [
    path("", MailingsListView.as_view(), name="mailings_list"),
    path(
        "newsletter/mailing/<int:pk>/",
        cache_page(60)(MailingsDetailView.as_view()),
        name="mailing_detail",
    ),
    path(
        "newsletter/mailing/create/",
        MailingsCreateView.as_view(),
        name="mailing_create",
    ),
    path(
        "newsletter/mailing/<int:pk>/update/",
        MailingsUpdateView.as_view(),
        name="mailing_update",
    ),
    path(
        "newsletter/mailing/<int:pk>/delete/",
        MailingsDeleteView.as_view(),
        name="mailing_delete",
    ),
    path("newsletter/client/", ClientListView.as_view(), name="clients_list"),
    path(
        "newsletter/client/<int:pk>/", ClientDetailView.as_view(), name="client_detail"
    ),
    path("newsletter/client/create/", ClientCreateView.as_view(), name="client_create"),
    path(
        "newsletter/client/<int:pk>/update/",
        ClientUpdateView.as_view(),
        name="client_update",
    ),
    path(
        "newsletter/client/<int:pk>/delete/",
        ClientDeleteView.as_view(),
        name="client_delete",
    ),
    path("newsletter/message/", MessagesListView.as_view(), name="messages_list"),
    path(
        "newsletter/message/<int:pk>/",
        MessagesDetailView.as_view(),
        name="message_detail",
    ),
    path(
        "newsletter/message/create/",
        MessagesCreateView.as_view(),
        name="message_create",
    ),
    path(
        "newsletter/message/<int:pk>/update/",
        MessagesUpdateView.as_view(),
        name="message_update",
    ),
    path(
        "newsletter/message/<int:pk>/delete/",
        MessagesDeleteView.as_view(),
        name="message_delete",
    ),
    # path(
    #     "newsletter/<int:pk>/unpublish/",
    #     UnpublishProductView.as_view(),
    #     name="product_unpublish",
    # ),
    # path(
    #     "catalog/<int:pk>/delete/delete/",
    #     DeleteProductView.as_view(),
    #     name="delete_product",
    # ),
]
