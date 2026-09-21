from django.contrib import messages
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext as _

from .models import Project, TodoCategory, TodoList


def home(request):
    projects = Project.objects.all()
    return render(
        request,
        "portfolio/home.html",
        {"projects": projects}
    )


def project_list(request):
    projects = Project.objects.all()
    return render(
        request,
        "portfolio/projects.html",
        {"projects": projects}
    )


def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    prev_project = (
        Project.objects.filter(id__lt=project.id).order_by('-id').first()
    )
    next_project = (
        Project.objects.filter(id__gt=project.id).order_by('id').first()
    )
    return render(
        request,
        'portfolio/project_detail.html',
        {
            'project': project,
            'prev_project': prev_project,
            'next_project': next_project,
        },
    )


def about(request):
    return render(
        request,
        "portfolio/about.html"
    )


def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        subject = f"Message from {name} ({email})"
        body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"

        try:
            send_mail(
                subject,
                body,
                email,
                ["admin@atelier.design"],
                fail_silently=False,
            )
            messages.success(request, _("Your message has been sent successfully!"))
        except Exception:
            messages.error(request, _("An error occurred. Please try again later."))

        return redirect("contact")

    return render(
        request,
        "portfolio/contact.html"
    )


def category_view(request):
    categories = TodoCategory.objects.all()

    if request.method == "POST":
        if "Add" in request.POST:
            name = request.POST.get("name")
            if name:
                TodoCategory.objects.create(name=name)
            return redirect("Category")

        if "Delete" in request.POST:
            checked_ids = request.POST.getlist("check")
            for cat_id in checked_ids:
                try:
                    cat = TodoCategory.objects.get(id=int(cat_id))
                    cat.delete()
                except Exception:
                    pass
            return redirect("Category")

    return render(request, "portfolio/category.html", {"categories": categories})


def todo_view(request):
    categories = TodoCategory.objects.all()
    todo_list = TodoList.objects.all()
    
    paginator = Paginator(todo_list, 5)
    page_number = request.GET.get("page")
    todos = paginator.get_page(page_number)

    if request.method == "POST":
        if "Add" in request.POST:
            title = request.POST.get("description")
            date = request.POST.get("date")
            category_name = request.POST.get("category_select")
            if title and date and category_name:
                try:
                    category_obj = TodoCategory.objects.get(name=category_name)
                    TodoList.objects.create(
                        title=title,
                        content=title,
                        due_date=date,
                        category=category_obj,
                    )
                except TodoCategory.DoesNotExist:
                    pass
            return redirect("TodoList")

        if "Delete" in request.POST:
            checked_ids = request.POST.getlist("checkedbox")
            for todo_id in checked_ids:
                try:
                    todo_item = TodoList.objects.get(id=int(todo_id))
                    todo_item.delete()
                except TodoList.DoesNotExist:
                    pass
            return redirect("TodoList")

    return render(
        request, 
        "portfolio/todo.html",
        {"todos": todos, "categories": categories},
    )