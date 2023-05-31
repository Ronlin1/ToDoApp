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


class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'task'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task'] = context['task'].filter(user=self.request.user)
        context['count'] = context['task'].filter(complete=False).count()
        
        # Implement Search
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['task'] = context['task'].filter(title__icontains = search_input)
            context['search_input'] = search_input
        return context

# Tas View details
class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'todo/task.html'

# Render Homepage 
def home(request):
    return render(request, 'todo/index.html')

# Creating the task view
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
    
    # render due time and reminder time inputs
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['due_date'].widget = DateTimeInput(attrs={'type': 'datetime-local'})
        form.fields['reminder_time'].widget = NumberInput(attrs={'type': 'number', 'min': 0})
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['datepickers'] = True
        return context
    
# Enable task edit
class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'complete',]
    success_url = reverse_lazy('task')
    
# Enable user task delete
class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('task')

class CustomLoginView(LoginView):
    """
    Custom login view for authentication.
    """

    template_name = 'todo/login.html'  # Template for the login page
    fields = "__all__"  # Specify the fields to be displayed on the login form
    redirect_authenticated_user = False  # Redirect authenticated user to success URL

    def get_success_url(self):
        """
        Get the success URL after successful login.
        """
        return reverse_lazy('task')  # Redirect to the 'task' URL


class RegisterPage(FormView):
    """
    View for user registration.
    """

    template_name = 'todo/register.html'  # Template for the registration page
    form_class = CustomUserCreationForm  # Form class for user registration
    redirect_authenticated_user = True  # Redirect authenticated user to success URL
    success_url = reverse_lazy('task')  # Redirect to the 'task' URL after successful registration

    def form_valid(self, form):
        """
        Perform actions when the form is valid.
        """
        user = form.save()  # Save the user registration form
        if user is not None:
            login(self.request, user)  # Login the user
        return super().form_valid(form)

    def form_invalid(self, form):
        """
        Perform actions when the form is invalid.
        """
        # print(form.errors)  # Print form errors for debugging purposes
        return super().form_invalid(form)

    def get(self, request, *args, **kwargs):
        """
        Handle GET request.
        """
        if self.request.user.is_authenticated:
            return redirect('task')  # Redirect to 'task' URL if user is already authenticated
        return super().get(request, *args, **kwargs)

# IMPLEMENT THIS LOG VIEWS LATER
class SystemLogsView(LoginRequiredMixin, ListView):
    model = SystemLog
    template_name = 'todo/sys_logs.html'
    context_object_name = 'system_logs'

    def get_queryset(self):
        return SystemLog.objects.filter(user=self.request.user)



# CONTINUE IMPLEMENTING THIS EVEN AFTER EXAM
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