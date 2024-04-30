from abc import ABC, abstractmethod

from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect


class EditObjectMixin(ABC):
    template_name = "profiles/edit_profile.html"

    @property
    @abstractmethod
    def success_url(self):
        pass

    @property
    @abstractmethod
    def form_instance_class(self):
        pass

    def get(self, request, *args, **kwargs):
        form = self.form_instance_class(instance=self.get_object())
        template = self.template_name
        return render(request, template, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_instance_class(request.POST, request.FILES, instance=self.get_object())
        if form.is_valid():
            instance = form.save(commit=False)
            if "image" in request.FILES:
                instance.image = request.FILES["image"]

            instance.save()
            form.save()
            return redirect(self.success_url)

    def get_object(self):
        raise NotImplementedError("Subclasses must implement get_object method")


class CreateObjectMixin(EditObjectMixin, ABC):
    template_name = None

    def get(self, request, *args, **kwargs):
        template = self.template_name
        form = self.form_instance_class
        return render(request, template, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_instance_class(request.POST)
        success_url = self.success_url
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            return redirect(success_url)
        # else:
        #     return HttpResponseBadRequest(form.errors)

    def get_object(self):
        pass
