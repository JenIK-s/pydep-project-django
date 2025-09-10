from django.shortcuts import redirect


class AnonymousRequiredMixin:
    redirect_url = 'lesson:profile'  # или другой URL

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.redirect_url)
        return super().dispatch(request, *args, **kwargs)
