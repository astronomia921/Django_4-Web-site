from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Image
from .forms import ImageCreateForm


@login_required
def image_list(request):
    template_1 = 'images/image/list_images.html'
    template_2 = 'images/image/list.html'

    images = Image.objects.all()
    paginator = Paginator(images, 8)
    page = request.GET.get('page')
    images_only = request.GET.get('images_only')
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        images = paginator.page(1)
    except EmptyPage:
        if images_only:
            return HttpResponse('')
        images = paginator.page(paginator.num_pages)
    if images_only:
        context = {
            'section': 'images',
            'images': images}
        return render(request, template_1, context)
    context = {
        'section': 'images',
        'images': images}
    return render(request, template_2, context)


@login_required
def image_create(request):
    template = 'images/image/create.html'
    if request.method == 'POST':
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_image = form.save(commit=False)
            new_image.user = request.user
            new_image.save()
            messages.success(request, 'Image added successfully')
            return redirect(new_image.get_absolute_url())
    else:
        form = ImageCreateForm(data=request.GET)
    context = {
        'section': 'images',
        'form': form}
    return render(request, template, context)


def image_detail(request, id, slug):
    template = 'images/image/detail.html'
    image = get_object_or_404(Image, id=id, slug=slug)
    context = {'section': 'images',
               'image': image}
    return render(request, template, context)


@login_required
@require_POST
def image_like(request):
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == 'like':
                image.users_like.add(request.user)
            else:
                image.users_like.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except Image.DoesNotExist:
            pass
    return JsonResponse({'status': 'error'})
