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
    MessageListView,
    MessageDetailView,
    MessageCreateView,
    MessageUpdateView,
    MessageDeleteView,
    MailingListView,
    MailingDetailView,
    MailingCreateView,
    MailingUpdateView,
    MailingDeleteView,
    MailingAttemptListView,
    MailingAttemptDetailView,
    SendMailingView,
)

app_name = NewsletterConfig.name

urlpatterns = [
    path("", MailingListView.as_view(), name="mailing_list"),
    path(
        "newsletter/mailing/<int:pk>/",
        cache_page(60)(MailingDetailView.as_view()),
        name="mailing_detail",
    ),
    path(
        "newsletter/mailings/create/",
        MailingCreateView.as_view(),
        name="mailing_create",
    ),
    path(
        "newsletter/mailing/<int:pk>/update/",
        MailingUpdateView.as_view(),
        name="mailing_update",
    ),
    path(
        "newsletter/mailing/<int:pk>/delete/",
        MailingDeleteView.as_view(),
        name="mailing_delete",
    ),
    path("newsletter/client/", ClientListView.as_view(), name="client_list"),
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
    path("newsletter/message/", MessageListView.as_view(), name="message_list"),
    path(
        "newsletter/message/<int:pk>/",
        MessageDetailView.as_view(),
        name="message_detail",
    ),
    path(
        "newsletter/message/create/",
        MessageCreateView.as_view(),
        name="message_create",
    ),
    path(
        "newsletter/message/<int:pk>/update/",
        MessageUpdateView.as_view(),
        name="message_update",
    ),
    path(
        "newsletter/message/<int:pk>/delete/",
        MessageDeleteView.as_view(),
        name="message_delete",
    ),
    path('mailing_attempt_list/', MailingAttemptListView.as_view(), name='mailing_attempt_list'),
    path('mailing_attempt/<int:pk>/detail/', MailingAttemptDetailView.as_view(),
         name='mailing_attempt_detail'),
    path('mailing/<int:pk>/send/', SendMailingView.as_view(), name='send_mailing'),
]
