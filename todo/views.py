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
from .models import SystemLog

from django.urls import reverse
from django.http import HttpResponseRedirect


# def login_from_email(request, user_id, todo_id):
#     # Check if user_id and todo_id exist and retrieve the associated user and todo instances
#     try:
#         user = User.objects.get(id=user_id)
#         todo = Todo.objects.get(id=todo_id)
#     except (User.DoesNotExist, Todo.DoesNotExist):
#         # User or todo does not exist, handle this case appropriately
#         return HttpResponse("User or Todo does not exist")

#     # Authenticate the user
#     user = authenticate(request, username=user.username, password=user.password)
#     if user is not None:
#         # Log the user in
#         login(request, user)
#         # Redirect the user to the appropriate todo item
#         return HttpResponseRedirect(reverse('todo-detail', args=[todo_id]))
#     else:
#         # Authentication failed, handle this case appropriately
#         return HttpResponse("Invalid login details")


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
        return response
    
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



