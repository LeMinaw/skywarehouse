from django.core.paginator  import Paginator
from django.core.exceptions import PermissionDenied
from django.shortcuts       import render, redirect
from django.http            import Http404, JsonResponse
from random                 import random
from operator               import attrgetter
from warehouse.forms        import *
from warehouse.models       import *
from warehouse.webhooks     import webhook

def home(request):
    blueprints_popular  = sorted(list(Blueprint.objects.all()), key=attrgetter('dwnlds'), reverse=True)[:3]
    blueprints_featured = Blueprint.objects.filter(pin=True).order_by('-added')[:3]
    blueprints_last     = Blueprint.objects.order_by('-added')[:3]

    return render(request, "warehouse/home.html", locals())


def main(request, slug=None, id=1):
    sort_by = 'added'
    reverse = True

    # Form data processing
    sort_form = ListSortForm(request.GET)
    if sort_form.is_valid():
        reverse = (sort_form.cleaned_data['order'] == "DSC")
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
    paginator = Paginator(blueprints, 2)
    blueprints = paginator.page(id)

    # Categories
    categories = Category.objects.all()

    return render(request, "warehouse/main.html", locals())


def blueprint(request, slug):
    try:
        blueprint = Blueprint.objects.get(slug=slug)
    except Blueprint.DoesNotExist:
        raise Http404("This blueprint does not exists. :(")

    if request.method == 'POST' and not request.user.is_authenticated:
        raise PermissionDenied("You must be logged in to comment or review.")

    old_review = None
    if request.user.is_authenticated:
        try:
            old_review = blueprint.reviews.get(author=request.user)
        except Review.DoesNotExist:
            pass
    review_form  = ReviewForm (prefix='review', instance=old_review)
    comment_form = CommentForm(prefix='comment')

    if 'review' in request.POST:
        review_form = ReviewForm(request.POST, prefix='review', instance=old_review)
    if 'comment' in request.POST:
        comment_form = CommentForm(request.POST, prefix='comment')

    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.author = request.user
        comment.blueprint = blueprint
        comment.save()
    if review_form.is_valid():
        review = review_form.save(commit=False)
        review.author = request.user
        review.blueprint = blueprint
        review.save()
    
    return render(request, "warehouse/blueprint.html", locals())


def files(request, slug):
    try:
        blueprint = Blueprint.objects.get(slug=slug)
    except Blueprint.DoesNotExist:
        raise Http404("This blueprint does not exists. :(")

    return render(request, "warehouse/files.html", locals())


def bp_edit(request, slug=None):
    if slug is not None:
        try:
            blueprint = Blueprint.objects.get(slug=slug)
        except Blueprint.DoesNotExist:
            raise Http404("This blueprint does not exists. :(")
        
        blueprint_form = BlueprintForm(
                request.POST or None,
                request.FILES or None,
                initial={'file': blueprint.last_file_version.file},
                instance=blueprint
        )
        
        if request.user != blueprint.author:
            raise PermissionDenied("You are not allowed to edit this blueprint. Try to log in.")

        if request.method == "POST" and blueprint_form.is_valid():
            blueprint_form.save()
            if 'file' in blueprint_form.changed_data:
                new_version_number = blueprint.last_file_version.number + 1
                file_version = FileVersion(file=request.FILES['file'], blueprint=blueprint, number=new_version_number)
                file_version.save()
            action = "modified"
            return render(request, "warehouse/bp_edit_done.html", locals())

    else:
        if not request.user.is_authenticated:
            raise PermissionDenied("Please log in before adding a blueprint.") # TODO: Use login decorator
        
        blueprint_form = BlueprintForm(request.POST or None, request.FILES or None)
        
        if request.method == "POST" and blueprint_form.is_valid():
            blueprint = blueprint_form.save(commit=False)
            blueprint.author = request.user
            blueprint.save()
            file_version = FileVersion(file=request.FILES['file'], blueprint=blueprint)
            file_version.save()
            webhook.send_new_blueprint(blueprint)
            action = "added"
            return render(request, "warehouse/bp_edit_done.html", locals())

    return render(request, "warehouse/bp_edit.html", locals())


def user(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise Http404("No user matched your query.")

    return render(request, "warehouse/user.html", locals())


def user_edit(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise Http404("No user matched your query.")
    
    if request.user != user:
        raise PermissionDenied("You are not allowed to edit this profile. Try to log in.")
    
    user_form = UserForm(request.POST or None, request.FILES or None, instance=user)

    if request.method == "POST" and user_form.is_valid():
        user_form.save()
        return render(request, "warehouse/user_edit_done.html", locals())
    
    return render(request, "warehouse/user_edit.html", locals())


def fav_edit(request, slug):
    if not request.user.is_authenticated:  # TODO: Use login decorator
        raise PermissionDenied("Please log in before modifying your favorites.")
    
    try:
        blueprint = Blueprint.objects.get(slug=slug)
        user = User.objects.get(username=request.user.username)
    except (Blueprint.DoesNotExist, User.DoesNotExist):
        raise Http404("Something went wrong with this request.")
    
    if blueprint in user.favs.all():
        user.favs.remove(blueprint)
        now_fav = False
    else:
        user.favs.add(blueprint)
        now_fav = True
    
    return JsonResponse({'now_fav': now_fav})


def download(request, slug, ver):
    try:
        blueprint = Blueprint.objects.get(slug=slug)
        version = blueprint.file_versions.get(number=ver)
    except (Blueprint.DoesNotExist, FileVersion.DoesNotExist):
        raise Http404("This file can't be found. :(")

    version.dwnlds += 1
    version.save()
    return redirect(version.file.url)


def about(request):
    return render(request, "warehouse/about.html", locals())
