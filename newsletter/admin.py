from django.contrib import admin

from newsletter.models import Client, Messages, Mailings, MailingsAttempt


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("email", "s_o_name", "comment")
    list_filter = ("email",)
    search_fields = ("email", "s_o_name")


@admin.register(Messages)
class MessagesAdmin(admin.ModelAdmin):
    list_display = ("subject",)
    list_filter = ("subject",)
    search_fields = ("subject",)


@admin.register(Mailings)
class MailingsAdmin(admin.ModelAdmin):
    list_display = (
        "first_send",
        "end_send",
        "status",
    )
    list_filter = (
        "client",
        "status",
    )
    search_fields = (
        "client",
    )


@admin.register(MailingsAttempt)
class MailingsAttemptAdmin(admin.ModelAdmin):
    list_display = (
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
