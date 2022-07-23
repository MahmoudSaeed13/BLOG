from django.contrib.auth.mixins import AccessMixin
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect

class AdminAccess(AccessMixin):
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request,'Only logged in admins can access this page', extra_tags='danger')
            return HttpResponseRedirect(reverse("login"))
        if not request.user.is_superuser:
            messages.error(request, 'Only admins can access this page', extra_tags='danger')
            return HttpResponseRedirect(reverse("home"))
        return super().dispatch(request, *args, **kwargs)

