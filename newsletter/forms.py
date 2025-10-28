from django import forms
from django.core.exceptions import ValidationError
from django.forms import BooleanField

from newsletter.models import Client, Messages, Mailings


class BootstrapFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fil_name, fild in self.fields.items():
            if isinstance(fild, BooleanField):
                fild.widget.attrs["class"] = "form-check-input"
            else:
                fild.widget.attrs["class"] = "form-control"


class ClientForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Client
        fields = ["email", "s_o_name"]

    # def clean(self):
    #     cleaned_data = super().clean()
    #     name = cleaned_data.get("s_o_name")
    #     description = cleaned_data.get("description")
    #
    #     word_error = ["казино", "криптовалюта", "крипта", "биржа", "дешево", "бесплатно", "обман", "полиция", "радар"]
    #     if name.lower() in word_error:
    #         self.add_error("name", f"Название продукта не может содержать слово {name}")
    #
    #     if description.lower() in word_error:
    #         self.add_error("description", f"Описание не может содержать слово {description}")
    #
    # def clean_price(self):
    #     price = self.cleaned_data.get("price")
    #     if price <= 0:
    #         raise ValidationError("Цена не может быть отрицательной или равна нулю.")
    #     return price


class MessagesForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Messages
        fields = ["subject", "text"]


class MailingsForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Mailings
        fields = ["first_send", "end_send", "status", "text", "client"]
