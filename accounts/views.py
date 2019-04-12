from django.views.generic import ListView, DetailView, FormView, TemplateView
from django.urls import reverse_lazy, reverse
from django.shortcuts import HttpResponseRedirect, render, get_object_or_404
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from .models import User, Profile
from .forms import ProfileForm


class RegisterView(FormView):
    form_class = UserCreationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('register')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


@login_required
def profile_view(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)
    form = ProfileForm(request.POST or None, instance=profile)
    orders = user.orders.all()
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('profile_page'))
    context = locals()
    return render(request, 'accounts/user_page.html', context)


@method_decorator(staff_member_required, name='dispatch')
class UserListView(ListView):
    template_name = ''
    model = User
    paginate_by = 50


@method_decorator(staff_member_required, name='dispatch')
class UserListView(DetailView):
    template_name = ''
    model = User


