from django.urls import reverse
from django.views.generic import FormView
from django.shortcuts import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from urllib.parse import urlencode
from accounts.forms import LoginForm


def custom_redirect(url_name, *args, **kwargs):
    url = reverse(url_name, args=args)
    params = urlencode(kwargs)
    return HttpResponseRedirect(url + "?%s" % params)


class SearchAndLoginMixin(FormView):
    form_class = LoginForm
    success_url = '/'

    def get(self, *args, **kwargs):
        if 'search_name' in self.request.GET:
            search_name = self.request.GET.get('search_name')
            return custom_redirect('site:search_page', search_name=search_name)
        return super().get(*args, **kwargs)

    def form_valid(self, form):
        username = form.cleaned_data.get('username', '')
        password = form.cleaned_data.get('password', '')
        user = authenticate(self.request, username=username, password=password)
        if user:
            login(self.request, user)
        else:
            messages.error(self.request, 'The credentials is invalid')
        return super().form_valid(form)
