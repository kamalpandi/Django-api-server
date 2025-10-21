from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import TodoForm
from .models import Todo

# Create your views here.

@login_required
def index(request):
    item_list = Todo.objects.order_by("-date")

    if request.method == "POST":
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.save()
            if request.headers.get("HX-Request"):
                return render(request, "todo/partials/todo_item.html", {"i": todo})

    form = TodoForm()
    page = {
        "forms": form,
        "list": item_list,
        "title": "TODO LIST",
    }
    return render(request, "todo/index.html", page)

@login_required
def remove(request, item_id):
    item = get_object_or_404(Todo, id=item_id)
    item.delete()

    if request.headers.get("HX-Request"):
        return HttpResponse("")
    else:
        messages.info(request, "Item removed !!!")
    return redirect("todo")
