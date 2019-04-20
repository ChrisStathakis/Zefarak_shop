from django.db.models import Q
from dal import autocomplete
from accounts.models import Profile


class ProfileAutoComplete(autocomplete.Select2QuerySetView):

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Profile.objects.none()

        qs = Profile.objects.all()
        if self.q:
            qs = qs.filter(Q(first_name__startwith=self.q) |
                           Q(last_name__startwith=self.q) |
                           Q(cellphone__startwith=self.q)
                           ).distinct()
        return qs