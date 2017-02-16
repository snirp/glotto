from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils.html import strip_tags
from .models import Youtube, Line
from .forms import YoutubeForm, TranslationAddForm


def index(request):
    return 'Hello world'


def view_item(request, media, i_id):
    if media == 'ytb':
        item = get_object_or_404(Youtube, pk=i_id)
        template = 'caption/view-item-youtube.html'
    else:
        raise Http404("Not valid media")

    if request.POST:
        form = TranslationAddForm(request.POST)
        if form.is_valid():
            print("valid form posted")
            form.instance.item = item
            form.instance.created_by = request.user
            form.instance.updated_by = request.user
            form.save()
    trans_dict = item.get_translation_dict_temp(blank_lines=True)
    form = TranslationAddForm()
    form.fields['language'].queryset = item.get_missing_languages()
    return render(request, template, {'form': form, 'item': item, 'trans_dict': trans_dict})


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


def edit_captions(request, media, i_id):
    if media == 'ytb':
        item = get_object_or_404(Youtube, pk=i_id)
        # If needed, define media-specific template for render method here:
        # template = 'caption/edit-captions-youtube.html'
    else:
        raise Http404("Not valid media")

    if request.method == 'POST':
        # TODO provide report with number lines added, edited and deleted in context
        stanza = False
        n = 1
        for line in (request.POST.get('captions', None)).splitlines():
            if not line or line.isspace():
                # Blank line means that next line starts a stanza,
                # and is not added itself as a line to the database.
                if n > 1:   # Skip leading blank lines
                    stanza = True
            else:
                # Trim user input to fit in db field (not being nice here)
                line = strip_tags(line)[:400]
                # The built-in get_or_create shortcut does not work for us,
                # since it requires updated_by and created_by values.
                try:
                    l = Line.objects.get(item=item, number=n)
                    if l.text != line or l.stanza != stanza:
                        # Something changed here, let's update it
                        l.text = line
                        l.stanza = stanza
                        l.updated_by = request.user
                        l.save()
                except ObjectDoesNotExist:
                    # It's a new line, let's create it
                    l = Line(item=item, number=n, text=line, stanza=stanza, updated_by=request.user,
                             created_by=request.user)
                    l.save()
                stanza = False
                n += 1
        # Cleanup possible higher numbered lines.
        # TODO Submitting a low/empty line count results in the
        #   deletion of many lines and translations. Acceptable?
        #   Should be resticted to priviledged users...
        Line.objects.filter(item=item, number__gte=n).delete()
    return render(request, 'caption/edit-captions.html', {'item': item})


# This view duplicates view_item with different template
def cue_captions(request, media, i_id):
    if media == 'ytb':
        item = get_object_or_404(Youtube, pk=i_id)
        return render(request, 'caption/cue-captions.html', {'item': item})
    raise Http404("Not valid media")


def cue_in(request):
    # TODO error handling:
    # - check user input
    # - check that line exists
    l_id = request.POST.get('lineId', None)
    time = int(request.POST.get('time', None))
    u_id = request.POST.get('userId', None)

    line = Line.objects.get(pk=l_id)
    line.cue_in = time
    line.updated_by = User.objects.get(pk=u_id)
    line.save()

    data = {'time': time}  # Return time in seconds for use in success handler
    return JsonResponse(data)


def cue_out(request):
    # TODO merge with cue_in: URL, view-code and template code
    l_id = request.POST.get('lineId', None)
    time = int(request.POST.get('time', None))
    u_id = request.POST.get('userId', None)

    line = Line.objects.get(pk=l_id)
    line.cue_out = time
    line.updated_by = User.objects.get(pk=u_id)
    line.save()

    data = {'time': time}  # Return time in seconds for use in success handler
    return JsonResponse(data)