from django.shortcuts import render, redirect, get_object_or_404
from .models import toode, projektid, mainvarvitabel, komplekteeri, task, projektivaade
from django.views.generic.list import ListView
from django.views.generic import UpdateView, DetailView, DeleteView
from .forms import komplekteerikogus, ExcelUploadForm, projektivaadeform, TaskSelectorForm, SelectionForm, CreateProjectForm
from django.views import View
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse, reverse_lazy
from django.contrib import messages

from .forms import ExcelUploadForm, CreateTaskForm, CreateUserForm
import pandas as pd


def pealeht(request):
    return render(request, 'pealeht/pealeht.html', {'view_name': 'Pealeht'})

def varvipealeht(request):
    return render(request, 'pealeht/varvipealeht.html', {'view_name': 'Värvitabel'})

class CustomLoginView(LoginView):
    template_name = 'pealeht/kasutajad/login.html'

def register(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # or wherever you want
    else:
        form = CreateUserForm()
    return render(request, 'pealeht/kasutajad/register.html', {'form': form})



class tootetabel(ListView):
    model = toode
    context_object_name = 'tooted'
    template_name = 'andmebaas/tooted/tooted.html'
    paginate_by = 15

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('desc', '')

        if query:
            queryset = queryset.filter(kirjeldus__icontains=query)

        sort = self.request.GET.get('sort', '')
        valid_sorts = ['kirjeldus', '-kirjeldus', 'tootekood', '-tootekood']
        
        if sort in valid_sorts:
            queryset = queryset.order_by(sort)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_name'] = 'Toodete Tabel'
        context['query'] = self.request.GET.get('desc', '')
        context['sort'] = self.request.GET.get('sort', '')
        return context
    
class toodedetail(DetailView):
    model = toode
    template_name = 'andmebaas/tooted/toode_detail.html'
    context_object_name = 'toode'

class toodeupdate(UpdateView):
    model = toode
    fields = ['tootekood', 'nimi', 'kirjeldus']
    template_name = 'andmebaas/tooted/toode_update.html'
    success_url = reverse_lazy('tooted')

def upload_excel(request):
    if request.method == 'POST' and request.FILES['excel_file']:
        # Read the Excel file
        excel_file = request.FILES['excel_file']
        df = pd.read_excel(excel_file)

        # Process the Excel data and add it to the database
        for _, row in df.iterrows():
            toode.objects.update_or_create(
                tootekood=row['tootekood'],  # Adjust field names to match your Excel columns
                defaults={
                    'nimi': row['nimi'],
                    'kirjeldus': row['kirjeldus']
                }
            )

        return HttpResponse("Data successfully uploaded!")
    
    form = ExcelUploadForm()
    return render(request, 'andmebaas/tooted/upload-toode.html', {'form': form})

def export_to_excel(request):
    # Get all products
    tooted = toode.objects.all().values('tootekood', 'nimi', 'kirjeldus')

    # Convert to pandas DataFrame
    df = pd.DataFrame(list(tooted))

    # Create HTTP response with Excel content
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="tooted.xlsx"'

    # Save DataFrame to Excel in-memory and write to response
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Tooted')

    return response


    
class projektitabel(ListView):
    model = projektid
    context_object_name = 'projektid'
    template_name = 'andmebaas/projektid/projektid.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_name'] = 'Projektid'
        return context
    
def createprojekt(request):
    if request.method == 'POST':
        form = CreateProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('projektid')
    else:
        form = CreateProjectForm()

    return render(request, 'andmebaas/projektid/create_projekt.html', {'form': form})





class taskitabel(ListView):
    model = task
    context_object_name = 'taskid'
    template_name = 'task/task/taskid.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_name'] = 'Taskid'
        return context

def view_komplekteeritudkogus(request):
    # Get the task.id from the URL query parameters
    task_id = request.GET.get('task.idurl')
    

    if task_id:
        # Filter items by the task_id
        items = komplekteeri.objects.filter(taskid_id=task_id)
    else:
        # If no task.id is provided, return all items
        items = komplekteeri.objects.all()

    # Create a form for each item
    forms = {item.id: komplekteerikogus(instance=item) for item in items}

    if request.method == 'POST':
        for item in items:
            form = forms[item.id]
            if f'save_{item.id}' in request.POST:
                form = komplekteerikogus(request.POST, instance=item)
                if form.is_valid():
                    form.save()

        # After saving the form, redirect to the same page with the task.idurl parameter
        if task_id:
            # Add the task.idurl to the redirect URL to preserve the filter
            return HttpResponseRedirect(f"{reverse('view_komplekteeritudkogus')}?task.idurl={task_id}")

    return render(request, 'task/komplekteeri/komplekteerimisvaade.html', {'forms': forms, 'task_id': task_id, 'view_name': task_id})


class projektivalik(ListView):
    model = projektid
    context_object_name = 'projektivalik'
    template_name = 'varvitabel/projektivalik.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_name'] = 'Projektivalik'
        return context



def projektivaadeview(request):
    projekt = request.GET.get('projekt')

    if projekt:
        items = projektivaade.objects.filter(projekt1__projekt=projekt)
    else:
        items = projektivaade.objects.all()

    # Create (item, selection form) pairs
    forms = [(item, SelectionForm(prefix=str(item.id))) for item in items]

    if request.method == 'POST':
        selected_ids = []

        for item, form in forms:
            form = SelectionForm(request.POST, prefix=str(item.id))
            if form.is_valid() and form.cleaned_data['selected']:
                selected_ids.append(item.id)

        if selected_ids:
            request.session['selected_items'] = selected_ids
            return redirect('task_selection')
        else:
            messages.warning(request, "Palun vali vähemalt üks toode.")

    return render(request, 'varvitabel/projektivaade.html', {
        'forms': forms,
        'projekt': projekt,
        'view_name': 'projektivaade'
    })

def choose_action_view(request):
    selected_ids = request.session.get('selected_items', [])

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'create_task':
            return redirect('create_task_form')
        elif action == 'change_deadline':
            return redirect('change_deadline_form')

    return render(request, 'varvitabel/choose_action.html', {
        'selected_ids': selected_ids
    })

def task_selection_view(request):
    if request.method == 'POST':
        form = TaskSelectorForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['create_new']:
                new_task = task.objects.create(
                    taskcreator=request.user,
                    responsible=form.cleaned_data['responsible'],
                    deadline=form.cleaned_data['deadline']
                )
                task_id = new_task.id
            else:
                task_id = form.cleaned_data['existing_task'].id

            # Save selected IDs and task in session
            request.session['selected_task'] = task_id
            return redirect('add_products_to_task')

    else:
        form = TaskSelectorForm()

    return render(request, 'varvitabel/select_task.html', {'form': form})

def create_task_form_view(request):
    selected_ids = request.session.get('selected_items', [])
    selected_items = projektivaade.objects.filter(id__in=selected_ids)

    if request.method == 'POST':
        form = CreateTaskForm(request.POST)
        if form.is_valid():
            # Create task
            new_task = task.objects.create(
                taskcreator=request.user,
                responsible=form.cleaned_data['responsible'],
                deadline=form.cleaned_data['deadline']
            )

            # Create komplekteeri objects for each selected projektivaade
            for item in selected_items:
                komplekteeri.objects.create(
                    taskid=new_task,
                    toode=item.toode,
                    kogus=0,  # default, or customize this later
                    komplekteeritudkogus=0
                )

            # Clean up
            del request.session['selected_items']

            return redirect('projektivaade')  # or to the task detail page
    else:
        form = CreateTaskForm()

    return render(request, 'varvitabel/create_task_form.html', {
        'form': form,
        'selected_items': selected_items
    })

def add_products_to_task_view(request):
    task_id = request.session.get('selected_task')
    selected_ids = request.session.get('selected_items', [])

    if not task_id:
        return redirect('task_selection')  # fallback if no task selected

    task_instance = task.objects.get(id=task_id)
    selected_items = projektivaade.objects.filter(id__in=selected_ids)

    if request.method == 'POST':
        for item in selected_items:
            komplekteeri.objects.create(
                taskid=task_instance,
                toode=item.toode,
                kogus=0,
                komplekteeritudkogus=0
            )

        # Clear session after use
        del request.session['selected_items']
        del request.session['selected_task']

        return redirect('projektivaade')  # or to a task overview

    return render(request, 'varvitabel/add_products.html', {
        'selected_items': selected_items,
        'task': task_instance
    })








"""
    
def projektivaadeview(request):
    projekt = request.GET.get('projekt')
    

    if projekt:
        # Filter items by the task_id
        items = projektivaade.objects.filter(projekt1__projekt=projekt)
    else:
        # If no task.id is provided, return all items
        items = projektivaade.objects.all()

    # Create a form for each item
    forms = [(item, komplekteerikogus(instance=item)) for item in items]




    if request.method == 'POST':
        for item in items:
            form = forms[item.projekt1]
            if f'save_{item.projekt1}' in request.POST:
                form = projektivaadeform(request.POST, instance=item)
                if form.is_valid():
                    form.save()

        # After saving the form, redirect to the same page with the task.idurl parameter
        if projekt:
            # Add the task.idurl to the redirect URL to preserve the filter
            return HttpResponseRedirect(f"{reverse('view_komplekteeritudkogus')}?projekt={projekt}")
    
    return render(request, 'varvitabel/projektivaade.html', {'forms': forms, 'projekt': projekt, 'view_name': projekt})
    

def get_queryset(self):
        # Get the 'projekt' filter value from the GET request
        projekt_filter = self.request.GET.get('projekt', '')

        # If a 'projekt' filter is provided, filter the queryset by that project
        if projekt_filter:
            return mainvarvitabel.objects.filter(projekt__id=projekt_filter)
        
        # Otherwise, return all records
        return mainvarvitabel.objects.all()

    


"""
