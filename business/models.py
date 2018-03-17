from datetime import date

from django.db import models
import django.db.models.options as options
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from django.conf import settings

from wagtail.contrib.wagtailroutablepage.models import RoutablePageMixin, route
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel, StreamFieldPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore import blocks
from wagtail.wagtailembeds.blocks import EmbedBlock
from wagtail.wagtailsnippets.edit_handlers import SnippetChooserPanel
from wagtail.wagtailadmin.edit_handlers import TabbedInterface, ObjectList
from wagtail.wagtailsearch import index

from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

from .snippets import *
from .blocks import QuoteBlock, CaptionImageBlock
from .forms import *

options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('description',)


class CarouselItem(LinkFields):
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    button = models.CharField(max_length=255, blank=True)
    embed_url = models.URLField("Video URL", blank=True)
    content = models.TextField(blank=True)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('embed_url'),
        FieldPanel('content'),
        FieldPanel('button'),
    ] + LinkFields.panels

    class Meta:
        abstract = True


class HomePage(Page):
    feed_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    subpage_types = [
        'SimplePage',
        'BlogIndexPage',
        'RegionalIndexPage',
        'SubmitFormPage',
    ]
    search_fields = []

    def blogs(self):
        return BlogPage.objects.live().order_by('-date')[:3]

    def get_context(self, request):
        context = super(HomePage, self).get_context(request)
        context['current_comps'] = CompPage.objects.descendant_of(self).live().filter(current=True)
        return context

    class Meta:
        description = "Home"
        verbose_name = "Home"


HomePage.content_panels = [
    FieldPanel('title', classname="full title"),
    InlinePanel(
        'carousel_items',
        label="Carousel items",
        help_text="Add the items appearing on the top carousel."
    ),
]

HomePage.promote_panels = [
    FieldPanel('slug'),
    FieldPanel('seo_title'),
    ImageChooserPanel('feed_image'),
    FieldPanel('search_description'),
]


class PageCarouselItem(Orderable, CarouselItem):
    page = ParentalKey('HomePage', related_name='carousel_items')


class BlogIndexPage(Page):
    intro = RichTextField(blank=True)
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    feed_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('subtitle'),
    ]
    subpage_types = [
        'BlogPage',
    ]

    @property
    def blogs(self):
        return BlogPage.objects.live().descendant_of(self).order_by('-date')

    def get_context(self, request):
        blogs = self.blogs
        # Filter by tag
        tag = request.GET.get('tag')
        if tag:
            blogs = blogs.filter(tags__name=tag)
        # Pagination
        page = request.GET.get('page')
        paginator = Paginator(blogs, settings.PAGINATION_PER_PAGE)
        try:
            blogs = paginator.page(page)
        except PageNotAnInteger:
            blogs = paginator.page(1)
        except EmptyPage:
            blogs = paginator.page(paginator.num_pages)
        context = super(BlogIndexPage, self).get_context(request)
        context['blogs'] = blogs
        return context

    class Meta:
        description = "Blog"
        verbose_name = "Blog"


BlogIndexPage.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('subtitle', classname="full"),
    FieldPanel('intro', classname="full"),
]

BlogIndexPage.promote_panels = [
    FieldPanel('slug'),
    FieldPanel('seo_title'),
    ImageChooserPanel('feed_image'),
    FieldPanel('search_description'),
]


class BlogPageRelatedLink(Orderable):
    link_page = models.ForeignKey(
        'BlogPage',
        on_delete=models.CASCADE,
        related_name='+',
    )
    page = ParentalKey('BlogPage', related_name='related_links')
    panels = [
        PageChooserPanel('link_page', 'business.BlogPage')
    ]


class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey('BlogPage', related_name='tagged_items')


class BlogPage(Page):
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateField("Post date", default=date.today)
    body = StreamField([
        ('paragraph', blocks.RichTextBlock()),
        ('image', CaptionImageBlock()),
        ('embed', EmbedBlock(icon='media')),
        ('quote', QuoteBlock()),
    ])
    excerpt = models.TextField(
        blank=True,
        help_text='The excerpt is used on the homepage miniatures only.'
    )
    intro = RichTextField(blank=True)
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)
    feed_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    author = models.ForeignKey(
        'Author',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='articles'
    )
    search_fields = Page.search_fields + [
        index.SearchField('body'),
        index.SearchField('intro'),
        index.SearchField('excerpt'),
        index.SearchField('subtitle'),
    ]
    subpage_types = []

    @property
    def blog_index(self):
        return self.get_parent().specific

    class Meta:
        description = "Blog post"
        verbose_name = "Blog post"


BlogPage.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('subtitle', classname="full"),
    FieldPanel('date'),
    FieldPanel('excerpt'),
    FieldPanel('intro', classname="full"),
    SnippetChooserPanel('author'),
    StreamFieldPanel('body'),
    FieldPanel('tags'),
    InlinePanel('related_links', label="Related links"),
]

BlogPage.promote_panels = [
    FieldPanel('slug'),
    FieldPanel('seo_title'),
    ImageChooserPanel('feed_image'),
    FieldPanel('search_description'),
]


class CompIndexPage(Page):
    intro = RichTextField(blank=True)
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    feed_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('subtitle'),
    ]
    subpage_types = [
        'CompPage',
    ]

    @property
    def pages(self):
        return CompPage.objects.live().descendant_of(self).filter(current=False).order_by('-year')

    def get_context(self, request):
        # Get pages
        pages = self.pages
        # Pagination
        page = request.GET.get('page')
        paginator = Paginator(pages, 10)  # Show 10 pages per page
        try:
            pages = paginator.page(page)
        except PageNotAnInteger:
            pages = paginator.page(1)
        except EmptyPage:
            pages = paginator.page(paginator.num_pages)
        # Update template context
        context = super(CompIndexPage, self).get_context(request)
        context['pages'] = pages
        context['current_comp'] = None
        try:
            context['current_comp'] = CompPage.objects.live().descendant_of(self).filter(current=True).first()
        except:
            pass
        return context

    class Meta:
        description = "Regional page"
        verbose_name = "Regional page"


CompIndexPage.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('subtitle', classname="full"),
    FieldPanel('intro', classname="full"),
]

CompIndexPage.promote_panels = [
    FieldPanel('slug'),
    FieldPanel('seo_title'),
    ImageChooserPanel('feed_image'),
    FieldPanel('search_description'),
]


class RegionalIndexPage(Page):
    subpage_types = ['CompIndexPage']
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    intro = RichTextField(blank=True)
    body = StreamField([
        ('paragraph', blocks.RichTextBlock()),
        ('image', CaptionImageBlock()),
        ('embed', EmbedBlock(icon='media')),
        ('quote', QuoteBlock()),
    ], blank=True)
    feed_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    search_fields = Page.search_fields + [
        index.SearchField('body'),
        index.SearchField('subtitle'),
    ]

    @property
    def pages(self):
        return CompIndexPage.objects.live().descendant_of(self).order_by('title')

    class Meta:
        description = "Regional Competitions"
        verbose_name = "Regions"
        verbose_name_plural = "Regions"


RegionalIndexPage.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('subtitle', classname="full"),
    FieldPanel('intro', classname="full"),
]

RegionalIndexPage.promote_panels = [
    FieldPanel('slug'),
    FieldPanel('seo_title'),
    ImageChooserPanel('feed_image'),
    FieldPanel('search_description'),
]


class CompPage(RoutablePageMixin, Page):
    subpage_types = []
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    current = models.BooleanField(default=False, help_text="Is this the current competition?")
    year = models.IntegerField("Year")
    winner = models.ForeignKey(
        'business.Team',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='winner_of'
    )
    body = StreamField([
        ('paragraph', blocks.RichTextBlock()),
        ('image', CaptionImageBlock()),
        ('embed', EmbedBlock(icon='media')),
        ('quote', QuoteBlock()),
    ], blank=True)
    feed_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    search_fields = Page.search_fields + [
        index.SearchField('body'),
        index.SearchField('subtitle'),
    ]

    @property
    def full_title(self):
        return '%s %s' % (self.get_parent().title, self.title)

    @route(r'^$')
    def current_page(self, request):
        return render(request, self.template, {'self': self})

    @route(r'^teams/$')
    def teams(self, request):
        return render(request, 'business/comp_page_teams.html', {'self': self})

    @property
    def get_next_results_by_date(self):
        return self.related_results.all().filter(date=self.get_next_date[0])

    @property
    def get_next_date(self):
        """
        Get either next date of the comp or last recent result date
        """
        dates = self.get_related_results().values('date').annotate(models.Count('date')).order_by('-date')
        for _date in dates:
            if _date['date'] > date.today():
                return (_date['date'], False)
        try:
            return (self.get_related_results().order_by('date').reverse()[0].date, True)
        except:
            return None

    @property
    def get_grouped_results(self):
        dates = self.get_related_results().values('date').annotate(models.Count('date')).order_by('-date')
        values = []
        for _date in dates:
            if _date['date__count']:
                values.append({
                        'date': _date['date'],
                        'values': self.get_related_results().filter(date=_date['date']),
                    })
        return values

    @property
    def get_grouped_teams(self):
        groups = self.get_related_teams().order_by('group').values('group').annotate(models.Count('group'))
        values = dict(((str(group['group']), self.get_related_teams().filter(group=group['group']))
                       for group in groups if group['group__count']))
        return values

    @property
    def get_finals_stats(self):
        """
        Get team total classification finals separated
        """
        teams = self.related_teams.all().order_by('group', 'final_classification')
        groups = teams.values('group').annotate(models.Count('group'))
        results_group = dict()

        for group in groups:
            results_group[str(group['group'])] = list()

            for team_group in teams:
                if team_group.group is group['group']:
                    results_group[str(team_group.group)].append(team_group.team)

        return results_group

    @property
    def get_stats(self):
        """
        Get team totals, by group and ordered by wins, finals separated
        """
        teams = self.get_related_teams()

        groups = self.get_related_teams().order_by('group').values('group').annotate(models.Count('group'))

        results_group = dict()

        for group in groups:
            results_group[str(group['group'])] = list()

        for team_group in teams:
            team_results_a = self.get_related_results().filter(is_final=False, team_one=team_group.team)
            team_results_b = self.get_related_results().filter(is_final=False, team_two=team_group.team)
            team_group.team.wins = 0
            team_group.team.losts = 0
            team_group.team.points = 0

            for result_a in team_results_a:
                team_group.team.wins += result_a.team_one_games
                team_group.team.losts += result_a.team_two_games
                team_group.team.points += result_a.team_one_games

                if result_a.team_one_games > result_a.team_two_games:
                    team_group.team.points += 2

            for result_b in team_results_b:
                team_group.team.wins += result_b.team_two_games
                team_group.team.losts += result_b.team_one_games
                team_group.team.points += result_b.team_two_games

                if result_b.team_two_games > result_b.team_one_games:
                    team_group.team.points += 2

            results_group[str(team_group.group)].append(team_group.team)

        for group in groups:
            results_group[str(group['group'])].sort(key=lambda x: x.points, reverse=True)

        return results_group

    def get_related_teams(self):
        return self.related_teams.all().order_by('group', 'team__name')

    def get_related_results(self):
        return self.related_results.all().order_by('date')

    @property
    def comp_index(self):
        # Find closest ancestor which is a comp index
        return self.get_ancestors().type(CompIndexPage).last()

    class Meta:
        description = "Competition"
        verbose_name = "Competition"

    content_panels = [
        FieldPanel('title', classname="full title"),
        FieldPanel('subtitle', classname="full"),
        FieldPanel('current'),
        FieldPanel('year'),
        SnippetChooserPanel('winner'),
        StreamFieldPanel('body'),
    ]

    team_panels = [
        InlinePanel(
            'related_teams',
            label="Teams competing",
            help_text="Add the teams involved on this competition."
        ),
    ]

    results_panels = [
        InlinePanel(
            'related_results',
            label="Results",
            help_text="Add the matches, with or without results, involved on this competition."
        ),
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        ObjectList(team_panels, heading='Teams'),
        ObjectList(results_panels, heading='Results'),
        ObjectList(Page.promote_panels, heading='Promote'),
        ObjectList(Page.settings_panels, heading='Settings', classname="settings"),
    ])


CompPage.promote_panels = Page.promote_panels + [
    ImageChooserPanel('feed_image'),
]


class TeamGroup(models.Model):
    team = models.ForeignKey(
        'Team',
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name='competitions'
    )
    group = models.IntegerField('Division', default=0)
    final_classification = models.IntegerField(default=0, help_text='To set once the comp is finished')
    panels = [
        FieldPanel('group'),
        SnippetChooserPanel('team'),
        FieldPanel('final_classification')
    ]

    class Meta:
        abstract = True


class CompPageTeam(Orderable, TeamGroup):
    page = ParentalKey('CompPage', related_name='related_teams')


class MatchResult(models.Model):
    date = models.DateField(default=date.today)
    team_one = models.ForeignKey(
        'Team',
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name='competitions_as_one'
    )
    team_two = models.ForeignKey(
        'Team',
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name='competitions_as_two'
    )
    team_one_games = models.IntegerField(default=0)
    team_two_games = models.IntegerField(default=0)
    is_final = models.BooleanField(default=False, null=False)
    panels = [
        FieldPanel('date'),
        FieldPanel('team_one'),
        FieldPanel('team_two'),
        FieldPanel('team_one_games'),
        FieldPanel('team_two_games'),
        FieldPanel('is_final')
    ]

    class Meta:
        abstract = True


class CompPageResult(Orderable, MatchResult):
    page = ParentalKey('CompPage', related_name='related_results')

    @property
    def team_one_name(self):
        return self.team_one.name

    @property
    def team_two_name(self):
        return self.team_two.name

    @property
    def title(self):
        return self.page.get_parent().title

    class Meta:
        description = "Result"
        verbose_name = "Result"


class SimplePage(Page):
    subpage_types = []
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    intro = RichTextField(blank=True)
    body = StreamField([
        ('paragraph', blocks.RichTextBlock()),
        ('image', CaptionImageBlock()),
        ('embed', EmbedBlock(icon='media')),
        ('quote', QuoteBlock()),
    ])
    feed_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
        index.SearchField('subtitle'),
    ]

    @property
    def pages(self):
        return SimplePage.objects.live().descendant_of(self)

    class Meta:
        description = "Plain page"
        verbose_name = "Plain page"


SimplePage.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('subtitle', classname="full"),
    FieldPanel('intro', classname="full"),
    StreamFieldPanel('body'),
]

SimplePage.promote_panels = Page.promote_panels + [
    ImageChooserPanel('feed_image'),
]
