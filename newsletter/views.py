from django.core.exceptions import PermissionDenied
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

from newsletter.forms import ClientForm, MessageForm, MailingForm, MailingManagerForm
from newsletter.models import Client, Message, Mailing, MailingAttempt
from newsletter.services import send_message


class ClientListView(ListView):
    model = Client
    template_name = "newsletter/client_list.html"
    context_object_name = "clientss"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        clientss = self.get_queryset()
        context['unique_clients'] = clientss.values('email').distinct().count()

        return context

    def get_queryset(self):
        if self.request.user.groups.filter(name='Manager').exists():
            return Client.objects.all()
        else:
            return Client.objects.filter(owner=self.request.user)


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy("newsletter:client_list")

    def form_valid(self, form):
        client = form.save()
        user = self.request.user
        client.owner = user
        client.save()
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy("newsletter:clients_list")

    def get_success_url(self):
        return reverse('newsletter:client_detail', args=[self.kwargs.get('pk')])


class ClientDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Client
    permission_required = "newsletter.client_delete"
    success_url = reverse_lazy("newsletter:client_list")
    context_object_name = "client"


class MessageListView(ListView):
    model = Message
    template_name = "newsletter/message_list.html"

    def get_queryset(self):
        if self.request.user.groups.filter(name='Manager').exists():
            return Message.objects.all()
        else:
            return Message.objects.filter(owner=self.request.user)


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("newsletter:message_list")

    def form_valid(self, form):
        message = form.save()
        user = self.request.user
        message.owner = user
        message.save()
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("newsletter:message_list")

    def get_success_url(self):
        return reverse('newsletter:message_detail', args=[self.kwargs.get('pk')])

class MessageDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Message
    permission_required = "newsletter.message_delete"
    success_url = reverse_lazy("newsletter:message_list")
    context_object_name = "message"


class MailingListView(ListView):
    model = Mailing
    template_name = "newsletter/mailing_list.html"
    context_object_name = 'mailings'

    def get_queryset(self):
        if self.request.user.groups.filter(name='Manager').exists():
            return Mailing.objects.all()
        else:
            return Mailing.objects.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mailings = self.get_queryset()
        context['total_mailings'] = mailings.count()
        context['active_mailings'] = mailings.filter(status='Запущена').count()


        return context


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing
    template_name = "newsletter/mailing_detail.html"

    def get_queryset(self):
        if self.request.user.groups.filter(name='Manager').exists():
            queryset = cache.get('mailing_list_for_manager')
            if not queryset:
                queryset = super().get_queryset()
                cache.set('mailing_list_for_manager', queryset, 60 * 15)  # Кешируем данные на 15 минут
            return queryset
        return super().get_queryset()


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = "newsletter/mailing_form.html"
    success_url = reverse_lazy("newsletter:mailing_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy("newsletter:mailing_list")

    def get_success_url(self):
        return reverse('mailing:mailing_detail', args=[self.kwargs.get('pk')])

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return MailingForm
        elif user.groups.filter(name='Manager').exists():
            return MailingManagerForm
        raise PermissionDenied


class MailingDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Mailing
    permission_required = "newsletter.mailing_delete"
    success_url = reverse_lazy("newsletter:mailing_list")


class MailingAttemptListView(LoginRequiredMixin, ListView):
    model = MailingAttempt
    template_name = 'newsletter/mailing_attempt_list.html'
    context_object_name = 'attempts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        attempts = self.get_queryset()
        context['total_attempts'] = attempts.count()
        context['successful_attempts'] = attempts.filter(status_new='Успешно').count()
        context['unsucessful_attempts'] = attempts.filter(status_new='Не успешно').count()
        context['sending_mails'] = sum(
            attempt.mailing.clients.count()
            for attempt in attempts.filter(status_new='Успешно')
        )
        return context

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            raise PermissionDenied("Вы не авторизованы")

        cache_key = f'mailing_attempts_user_{self.request.user.pk}'
        queryset = cache.get(cache_key)
        if not queryset:
            if self.request.user.groups.filter(name='Manager').exists():
                queryset = MailingAttempt.objects.all()
            else:
                queryset = MailingAttempt.objects.filter(mailing__owner=self.request.user).order_by('-start_time')
            cache.set(cache_key, queryset, 60 * 15)

        return queryset


class MailingAttemptDetailView(LoginRequiredMixin, DetailView):
    model = MailingAttempt
    template_name = 'newsletter/mailing_attempt_detail.html'


class SendMailingView(View):
    template_name = 'newsletter/send_mailing.html'

    def get(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk, owner=request.user)

        success = send_message(mailing.pk, request)

        if success:
            print('Рассылка успешно отправлена')
        else:
            print('Рассылка не отправлена')

        return redirect('newsletter:mailing_list')