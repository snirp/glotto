from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import Youtube, Item
from .forms import YoutubeForm


def index(request):
    return 'Hello world'


def view_item(request, media, i_id):
    if media == 'ytb':
        item = get_object_or_404(Youtube, pk=i_id)
        return render(request, 'caption/view-item-youtube.html', {'item': item})
    raise Http404("Not valid media")


def get_play_context(item):
    lines = item.line_set.filter(cue_in__isnull=False).order_by('cue_in')
    times = [l.cue_in for l in lines]
    texts = [l.text for l in lines]
    # TODO-improve: We now pass every full translation to the template.
    #   This grows linearly with added translations, so we may consider only
    #   providing the primary translation and back up with an ajax call to
    #   load any replacement language.
    translations = item.get_translation_dict(ordering='line__cue_in')  # key: language code
                                                                       # value: list of linetrans strings
    return {'item': item, 'times': times, 'texts': texts, 'translations': translations}


def play_item(request, media, i_id):
    if media == 'ytb':
        i = get_object_or_404(Youtube, pk=i_id)
        context = get_play_context(i)
        return render(request, 'caption/play-item-youtube.html', context)


def edit_item(request, media, i_id=None):
    if media == 'ytb':
        if i_id:
            item = get_object_or_404(Youtube, pk=i_id)
            template = 'caption/edit-item-youtube.html'
        else:
            item = Youtube()
            template = 'caption/add-item-youtube.html'
        form = YoutubeForm(request.POST or None, instance=item)
    # Add new media type here inside similar if-statement
    else:
        raise Http404("Not valid media")

    if request.POST and form.is_valid():
        print(form.instance)
        form.instance.media_type = media
        form.instance.created_by = request.user
        form.instance.updated_by = request.user
        form.save()
        if i_id:
            # Item was added
            return redirect(reverse('view-item', kwargs={'media': media, 'i_id': item.id}))
        # Item was updated
        return redirect(reverse('view-item', kwargs={'media': media, 'i_id': item.id}))
    return render(request, template, {'form': form, 'item': item})
