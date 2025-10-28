from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.cache import cache
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
    View,
)

from newsletter.forms import ClientForm, MessagesForm, MailingsForm
from newsletter.models import Client, Messages, Mailings

# from newsletter.services import get_products_by_category


class ClientListView(ListView):
    model = Client
    template_name = "newsletter/clients_list.html"
    context_object_name = "clients"

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     product_category = context['products'][0].category
    #     context["category"] = get_products_by_category(product_category)
    #     return context
    #
    # def get_queryset(self):
    #     queryset = cache.get("products_queryset")
    #     if not queryset:
    #         queryset = super().get_queryset()
    #         cache.set("products_queryset", queryset, 60)
    #     return queryset


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy("newsletter:client_list")

    # def form_valid(self, form):
    #     form.instance.owner = self.request.user
    #     return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy("newsletter:client_list")

    # def get_object(self, queryset=None):
    #     obj = super().get_object(queryset)
    #     if not obj.owner == self.request.user:
    #         return HttpResponseForbidden("У вас нет прав для редактирование этого продукта")
    #     return obj


class ClientDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Client
    permission_required = "newsletter.client_delete"
    success_url = reverse_lazy("newsletter:client_list")
    context_object_name = "client"

    # def get_object(self, queryset=None):
    #     obj = super().get_object(queryset)
    #     if not obj.owner == self.request.user:
    #         return HttpResponseForbidden("У вас нет прав для удаление этого продукта")
    #     return obj


class MessagesListView(ListView):
    model = Messages
    template_name = "newsletter/messages_list.html"
    context_object_name = "messages"

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     product_category = context['products'][0].category
    #     context["category"] = get_products_by_category(product_category)
    #     return context
    #
    # def get_queryset(self):
    #     queryset = cache.get("products_queryset")
    #     if not queryset:
    #         queryset = super().get_queryset()
    #         cache.set("products_queryset", queryset, 60)
    #     return queryset


class MessagesDetailView(LoginRequiredMixin, DetailView):
    model = Messages


class MessagesCreateView(LoginRequiredMixin, CreateView):
    model = Messages
    form_class = MessagesForm
    success_url = reverse_lazy("newsletter:messages_list")

    # def form_valid(self, form):
    #     form.instance.owner = self.request.user
    #     return super().form_valid(form)


class MessagesUpdateView(LoginRequiredMixin, UpdateView):
    model = Messages
    form_class = MessagesForm
    success_url = reverse_lazy("newsletter:messages_list")

    # def get_object(self, queryset=None):
    #     obj = super().get_object(queryset)
    #     if not obj.owner == self.request.user:
    #         return HttpResponseForbidden("У вас нет прав для редактирование этого продукта")
    #     return obj


class MessagesDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Messages
    permission_required = "newsletter.message_delete"
    success_url = reverse_lazy("newsletter:messages_list")
    context_object_name = "message"

    # def get_object(self, queryset=None):
    #     obj = super().get_object(queryset)
    #     if not obj.owner == self.request.user:
    #         return HttpResponseForbidden("У вас нет прав для удаление этого продукта")
    #     return obj


class MailingsListView(ListView):
    model = Mailings
    template_name = "newsletter/mailings_list.html"
    context_object_name = "mailings"

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     product_category = context['products'][0].category
    #     context["category"] = get_products_by_category(product_category)
    #     return context
    #
    # def get_queryset(self):
    #     queryset = cache.get("products_queryset")
    #     if not queryset:
    #         queryset = super().get_queryset()
    #         cache.set("products_queryset", queryset, 60)
    #     return queryset


class MailingsDetailView(LoginRequiredMixin, DetailView):
    model = Mailings


class MailingsCreateView(LoginRequiredMixin, CreateView):
    model = Mailings
    form_class = MailingsForm
    success_url = reverse_lazy("newsletter:mailings_list")

    # def form_valid(self, form):
    #     form.instance.owner = self.request.user
    #     return super().form_valid(form)


class MailingsUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailings
    form_class = MailingsForm
    success_url = reverse_lazy("newsletter:mailings_list")

    # def get_object(self, queryset=None):
    #     obj = super().get_object(queryset)
    #     if not obj.owner == self.request.user:
    #         return HttpResponseForbidden("У вас нет прав для редактирование этого продукта")
    #     return obj


class MailingsDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Mailings
    permission_required = "newsletter.mailing_delete"
    success_url = reverse_lazy("newsletter:mailings_list")
    context_object_name = "mailing"

    # def get_object(self, queryset=None):
    #     obj = super().get_object(queryset)
    #     if not obj.owner == self.request.user:
    #         return HttpResponseForbidden("У вас нет прав для удаление этого продукта")
    #     return obj
