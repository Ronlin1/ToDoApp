from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Task
from .forms import CustomUserCreationForm
from django.forms.widgets import DateTimeInput, NumberInput
from django.contrib.auth.decorators import login_required
from .models import SystemLog
from datetime import timedelta
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone
from threading import Thread


# from .forms import ReminderForm

class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'task'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task'] = context['task'].filter(user=self.request.user)
        context['count'] = context['task'].filter(complete=False).count()
    
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['task'] = context['task'].filter(title__icontains = search_input)
            context['search_input'] = search_input
        return context

class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'todo/task.html'
    
def home(request):
    return render(request, 'todo/index.html')

class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'due_date', 'reminder_time']
    success_url = reverse_lazy('task')
    template_name = 'todo/task_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.email = self.request.user.email
        response = super().form_valid(form)

    #     if form.cleaned_data['reminder_time'] > 0:
    #         reminder_time = form.instance.due_date - timezone.timedelta(minutes=form.cleaned_data['reminder_time'])
    #         Thread(target=self.send_reminder_email, args=(form.instance.user.pk, form.instance.pk, reminder_time)).start()

    #     messages.success(self.request, 'Task created successfully.')
        return response
    
    # def send_reminder_email(self, user_id, task_id, reminder_time):
    #     user = User.objects.get(pk=user_id)
    #     task = Task.objects.get(pk=task_id)
    #     subject = f'Reminder: Task "{task.title}" due soon'
    #     message = render_to_string('todo/email_reminder.html', {
    #         'user': user,
    #         'task': task,
    #         'reminder_time': reminder_time
    #     })
    #     from_email = settings.EMAIL_HOST_USER
    #     recipient_list = [user.email]
    #     send_mail(subject, message, from_email, recipient_list, fail_silently=False)


    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['due_date'].widget = DateTimeInput(attrs={'type': 'datetime-local'})
        form.fields['reminder_time'].widget = NumberInput(attrs={'type': 'number', 'min': 0})
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['datepickers'] = True
        return context

class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'complete',]
    success_url = reverse_lazy('task')


class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('task')


# class TaskDelete(LoginRequiredMixin, DeleteView):
#     model = Task
#     # template_name = 'todo/task_confirm_delete.html'
#     context_object_name = 'task'
#     success_url = reverse_lazy('task')
    
#     def form_valid(self, form):
#         if self.request.user != self.get_object().user:
#             messages.error(self.request, "You don't have permission to delete this task.")
#             return redirect("task")
#         messages.success(self.request, "The task was deleted successfully.")
#         return super().form_valid(form)


class CustomLoginView(LoginView):
    template_name = 'todo/login.html'
    fields = "__all__"
    redirect_authenticated_user = False

    def get_success_url(self):
        return reverse_lazy('task')

class RegisterPage(FormView):
    template_name = 'todo/register.html'
    form_class = CustomUserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('task')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)
    
    def form_invalid(self, form):
        # print(form.errors)
        return super().form_invalid(form)

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('task')
        return super().get(request, *args, **kwargs)
    

class SystemLogsView(LoginRequiredMixin, ListView):
    model = SystemLog
    template_name = 'todo/sys_logs.html'
    context_object_name = 'system_logs'

    def get_queryset(self):
        return SystemLog.objects.filter(user=self.request.user)



