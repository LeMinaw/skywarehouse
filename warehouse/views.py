from django.shortcuts       import render
from django.core.paginator  import Paginator
from django.http            import Http404
from django.core.exceptions import PermissionDenied
from math                   import ceil
from random                 import random
from operator               import attrgetter
from warehouse.forms        import *
from warehouse.models       import *


def nest(iterable, count):
    """Makes a list of lists of <count> elements out of an input <iterable>."""
    outLen = int(ceil(len(iterable) / count))
    return [iterable[i * count : (i+1) * count] for i in range(outLen)]


def home(request):
    blueprints_popular  = sorted(list(Blueprint.objects.all()), key=attrgetter('dwnlds'), reverse=True)[:3]
    blueprints_featured = Blueprint.objects.filter(pin=True).order_by('-added')[:3]
    blueprints_last     = Blueprint.objects.order_by('-added')[:3]

    return render(request, "warehouse/home.html", locals())


def main(request, slug=None, id=1):
    sort_by = 'added'
    reverse = True

    # Form data processing
    if request.method == "POST":
        sort_form = ListSortForm(request.POST)
        if sort_form.is_valid():
            reverse = (sort_form.cleaned_data['reverse_order'] == "DSC")
            sort_by = sort_form.cleaned_data['sort_by']
    else:
        sort_form = ListSortForm()

    # Sort function definition
    if sort_by ==  'random':
        sort_fn = lambda x: random()
    else:
        sort_fn = attrgetter(sort_by)

    # Category filtering
    if slug is None:
        blueprints = Blueprint.objects.all()
    else:
        blueprints = Blueprint.objects.filter(categ__slug=slug)
    blueprints = sorted(blueprints, key=sort_fn, reverse=reverse)

    # Pagination
    paginator = Paginator(blueprints, 12)
    blueprints = paginator.page(id).object_list

    # Categories
    categories = Category.objects.all()

    return render(request, "warehouse/main.html", locals())


def blueprint(request, slug):
    try:
        blueprint = Blueprint.objects.get(slug=slug)
    except Blueprint.DoesNotExist:
        raise Http404("This blueprint does not exists. :(")

    return render(request, "warehouse/blueprint.html", locals())


def files(request, slug):
    try:
        blueprint = Blueprint.objects.get(slug=slug)
    except Blueprint.DoesNotExist:
        raise Http404("This blueprint does not exists. :(")

    return render(request, "warehouse/files.html", locals())


def edit(request, slug=None):
    if slug is not None:
        try:
            blueprint = Blueprint.objects.get(slug=slug)
        except Blueprint.DoesNotExist:
            raise Http404("This blueprint does not exists. :(")
        blueprint_form = BlueprintForm(request.POST or None, request.FILES or None, instance=blueprint)
        if request.user is not blueprint.author:
            raise PermissionDenied("You are not allowed to edit this blueprint.")

        if request.method == "POST" and blueprint_form.is_valid():
                blueprint_form.save()
                if blueprint_form.file.has_changed():
                    file_version = FileVersion(file=request.FILES['file'], blueprint=blueprint)
                    file_version.save()

        else:
            blueprint_form = BlueprintForm(initial={'file': blueprint.last_file_version}, instance=blueprint)

    else:
        if not request.user.is_authenticated():
            raise PermissionDenied("Please log in before adding a blueprint.") # TODO: Use login decorator
        blueprint_form = BlueprintForm(request.POST or None, request.FILES or None)
        if request.method == "POST" and blueprint_form.is_valid():
            blueprint = blueprint_form.save(commit=False)
            blueprint.author = request.user
            blueprint.save()
            file_version = FileVersion(file=request.FILES['file'], blueprint=blueprint)
            file_version.save()

    return render(request, "warehouse/edit.html", locals())


def user(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise Http404("No user matched your query.")

    return render(request, "warehouse/user.html", locals())


def useredit(request, username):
    pass


def about(request):
    return render(request, "warehouse/about.html", locals())
