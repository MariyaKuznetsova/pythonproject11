from django.contrib import admin

from newsletter.models import Client, Message, Mailing, MailingAttempt


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "s_o_name", "comment")
    list_filter = ("email",)
    search_fields = ("email", "s_o_name")


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "subject",)
    list_filter = ("subject",)
    search_fields = ("subject",)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "first_send",
        "end_send",
        "status",
    )
    list_filter = (
        "clients",
        "status",
    )
    search_fields = (
        "clients",
    )


@admin.register(MailingAttempt)
class MailingAttemptAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "start_time",
        "post_response",
    )
    list_filter = (
        "start_time",
        "post_response",
    )
    search_fields = (
        "start_time",
        "post_response",
    )
