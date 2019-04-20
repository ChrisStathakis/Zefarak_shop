from django.db.models import Q
from dal import autocomplete
from accounts.models import Profile


class ProfileAutoComplete(autocomplete.Select2QuerySetView):

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Profile.objects.none()

        qs = Profile.objects.all()
        if self.q:
            self.q = self.q.capitalize()
            qs = qs.filter(Q(first_name__startswith=self.q) |
                           Q(last_name__startswith=self.q) |
                           Q(cellphone__startswith=self.q)
                           ).distinct()
        return qs
