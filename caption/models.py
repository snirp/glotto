from django.contrib.auth.models import User
from django.db import models
from django.db.models import Count


class Language(models.Model):
    code = models.SlugField(max_length=5, unique=True)
    name = models.CharField(max_length=50, unique=True)
    flag = models.ImageField(upload_to='flags', null=True, blank=True)

    def __str__(self):
        return self.name

    def item_count(self):
        return Count(self.item_set.all())

    class Meta:
        ordering = ['name']


class UserContent(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, related_name='%(class)s_creator')
    updated_by = models.ForeignKey(User, related_name='%(class)s_updater')

    class Meta:
        abstract = True


class Artist(UserContent):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Item(UserContent):
    title = models.CharField(max_length=200)
    language = models.ForeignKey(Language)
    artists = models.ManyToManyField(Artist, blank=True)
    played = models.IntegerField(default=0)
    media_type = models.CharField(max_length=3, choices=(
        ('ytb', 'youtube', ),
        ('mp3', 'mp3', ),
    ))

    def __str__(self):
        return self.title

    def percentage_cued(self):
        l_count = self.line_set.count()
        if not l_count:
            return 0
        return int((self.line_set.filter(cue_in__isnull=False).count() / l_count) * 100)

    def first_artist(self):
        if self.artists.all():
            return self.artists.all()[0]

    def get_missing_languages(self):
        return Language.objects.exclude(translation__in=self.translation_set.all()).exclude(pk=self.language.pk)

    def full_translations(self):
        fulltrans = Linetrans.objects.filter(line__item=self).values('translation').annotate(total=Count('translation')). \
                order_by('total').filter(total=self.line_set.count())
        return Translation.objects.filter(pk__in=[x['translation'] for x in fulltrans])

    def get_translation_dict(self, ordering='line__number', blank_lines=False):
        trans = {}
        for t in self.full_translations():
            lts = Linetrans.objects.filter(translation=t).order_by(ordering)
            strings = []
            for lt in lts:
                if blank_lines and lt.line.stanza:
                    strings.append("")
                strings.append(lt.text)
            trans[t.language.code] = strings
        return trans

    def get_translation_dict_temp(self, ordering='line__number', blank_lines=False):
        trans = {}
        for t in self.translation_set.all():
            lts = Linetrans.objects.filter(translation=t).order_by(ordering)
            strings = []
            for lt in lts:
                if blank_lines and lt.line.stanza:
                    strings.append("")
                strings.append(lt.text)
            trans[t.language.code] = strings
        return trans

    class Meta:
        ordering = ['title']


class Youtube(Item):
    key = models.CharField(max_length=11, null=True, blank=True, unique=True)

    def __str__(self):
        return self.title

# Further inherited classes: Vimeo, Mp3, Soundcloud, etc


class Line(UserContent):
    number = models.IntegerField()
    item = models.ForeignKey(Item)
    text = models.CharField(max_length=400, null=True, blank=True)
    cue_in = models.IntegerField(null=True, blank=True)  # In tenths of seconds
    cue_out = models.IntegerField(null=True, blank=True)
    stanza = models.BooleanField(default=False)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['item', 'number']
        unique_together = ('item', 'number', )


class Translation(UserContent):
    item = models.ForeignKey(Item)
    language = models.ForeignKey(Language)
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title

    def lines_remaining(self):
        return self.item.line_set.count()-self.linetrans_set.count()

    def percentage_complete(self):
        l_count = self.item.line_set.count()
        if not l_count:
            return 0
        return int((self.linetrans_set.count()/l_count)*100)

    class Meta:
        ordering = ['item', 'language']
        unique_together = ('item', 'language',)  # One translation per item & language


class Linetrans(UserContent):
    line = models.ForeignKey(Line)
    translation = models.ForeignKey(Translation)
    text = models.CharField(max_length=400)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['line']
        verbose_name_plural = 'Linetranslations'


class Playlist(models.Model):
    owner = models.ForeignKey(User)
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    items = models.ManyToManyField(Item, blank=True)

    def __str__(self):
        return self.name

    def item_count(self):
        return self.items.count()

    def follower_count(self):
        return self.member_set.count()

    def language(self):
        if not self.items.all():
            return None
        return self.items.all()[0].language
        # TODO: check all songs for language and return None if more than 1 language or most used language (?)


class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(Item, blank=True)
    primary = models.ForeignKey(Language, related_name='primary')
    subscriptions = models.ManyToManyField(Playlist, blank=True)
    languages = models.ManyToManyField(Language, related_name='languages')

    def __str__(self):
        return self.user.__str__()