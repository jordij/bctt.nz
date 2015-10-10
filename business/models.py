from datetime import date

from django.db import models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from django.conf import settings

import django.db.models.options as options

from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel, StreamFieldPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailembeds.blocks import EmbedBlock
from wagtail.wagtailsnippets.edit_handlers import SnippetChooserPanel
from wagtail.wagtailadmin.edit_handlers import TabbedInterface, ObjectList
from wagtail.contrib.wagtailroutablepage.models import RoutablePageMixin, route


from wagtail.wagtailsearch import index

from modelcluster.fields import ParentalKey
from modelcluster.tags import ClusterTaggableManager
from taggit.models import TaggedItemBase

from .utilities import *
from .snippets import *
from .blocks import *
from .forms import *

options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('description',)


class CarouselItem(LinkFields):
    """
    A set of carousel images
    """
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
    """
    HomePage class
    """
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
        'CompIndexPage',
        'SubmitFormPage',
    ]
    search_fields = ()

    def blogs(self):
        # Get latest blogs
        return BlogPage.objects.live().order_by('-date')[:3]

    def get_context(self, request):

        context = super(HomePage, self).get_context(request)

        # Get current comp
        try:
            current_comp = CompPage.objects.live().filter(current=True)[0]
        except:
            return context

        # Update template context
        context['current_comp'] = current_comp
        return context

    class Meta:
        description = "The top level homepage for your site"
        verbose_name = "Homepage"

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


#  Some classes to use as fields (Carousel, Related links and Tags)
class PageCarouselItem(Orderable, CarouselItem):
    page = ParentalKey('HomePage', related_name='carousel_items')


# BlogIndex page

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
    search_fields = Page.search_fields + (
        index.SearchField('intro'),
        index.SearchField('subtitle'),
    )
    subpage_types = [
        'BlogPage',
    ]

    @property
    def blogs(self):
        # Get list of live blog pages that are descendants of this page
        blogs = BlogPage.objects.live().descendant_of(self)

        # Order by most recent date first
        blogs = blogs.order_by('-date')

        return blogs

    def get_context(self, request):
        # Get blogs
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

        # Update template context
        context = super(BlogIndexPage, self).get_context(request)
        context['blogs'] = blogs
        return context

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


# Blog page

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
        ('paragraph', SimpleRichTextBlock()),
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

    search_fields = Page.search_fields + (
        index.SearchField('body'),
        index.SearchField('intro'),
        index.SearchField('excerpt'),
        index.SearchField('subtitle'),
    )

    subpage_types = []


    @property
    def blog_index(self):
        # Find closest ancestor which is a blog index
        return self.get_ancestors().type(BlogIndexPage).last()

BlogPage.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('subtitle', classname="full"),
    FieldPanel('date'),
    FieldPanel('excerpt'),
    FieldPanel('intro', classname="full"),
    SnippetChooserPanel('author', Author),
    StreamFieldPanel('body'),
    FieldPanel('tags'),
    InlinePanel(BlogPage, 'related_links', label="Related links"),
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
    search_fields = Page.search_fields + (
        index.SearchField('intro'),
        index.SearchField('subtitle'),
    )
    subpage_types = [
        'CompPage',
    ]

    @property
    def pages(self):
        # Get list of live comp pages that are descendants of this page
        pages = CompPage.objects.live().descendant_of(self)

        # Order by most recent date first
        pages = pages.order_by('-year')

        return pages

    def serve(self, request, *args, **kwargs):
        """
        Override if there's a current comp
        """
        try:
            current_comp = CompPage.objects.live().descendant_of(self).filter(current=True)[0]
            return redirect(current_comp.url, *args, **kwargs)
        except:
            return super(CompIndexPage, self).serve(request, *args, **kwargs)

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
        return context

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


# Comp page

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
        ('paragraph', SimpleRichTextBlock()),
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
    search_fields = Page.search_fields + (
        index.SearchField('body'),
        index.SearchField('subtitle'),
    )

    @route(r'^$')
    def current_page(self, request):

        context = {}
        context['self'] = self

        return render(request, self.template, context)

    @route(r'^teams/$')
    def teams(self, request):

        context = {}
        context['self'] = self

        return render(request, 'business/comp_page_teams.html', context)

    @property
    def get_next_results_by_date(self):
        cur_date = self.get_next_date
        return self.related_results.all().filter(date=cur_date[0])

    @property
    def get_next_date(self):
        """
        Get either next date of the comp or last recent result date
        """
        dates = self.get_related_results().order_by('date').values('date').annotate(models.Count('date'))
        for _date in dates:
            if _date['date'] > date.today():
                return (_date['date'], False)
        try:
            return (self.get_related_results().order_by('date').reverse()[0].date, True)
        except:
            return None

    @property
    def get_grouped_results(self):
        dates = self.get_related_results().values('date').annotate(models.Count('date'))
        values = dict(((str(date['date']), self.get_related_results().filter(date=date['date'])) for date in dates if date['date__count']))
        return values

    @property
    def get_grouped_teams(self):
        groups = self.get_related_teams().values('group').annotate(models.Count('group'))
        values = dict(((str(group['group']), self.get_related_teams().filter(group=group['group'])) for group in groups if group['group__count']))
        return values

    @property
    def get_stats(self):
        """
        Get team totals, by group and ordered by wins, finals separated
        """
        teams = self.get_related_teams()

        groups = self.get_related_teams().values('group').annotate(models.Count('group'))

        results_group = dict()

        for group in groups:
            results_group[str(group['group'])] = list()

        for team_group in teams:
            team_group.team
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

    content_panels = [
        FieldPanel('title', classname="full title"),
        FieldPanel('subtitle', classname="full"),
        FieldPanel('current'),
        FieldPanel('year'),
        SnippetChooserPanel('winner', Team),
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
    group = models.IntegerField(default=0)
    panels = [
        FieldPanel('group'),
        SnippetChooserPanel('team', Team),
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


# Simple page

class SimplePage(Page):
    subpage_types = []

    subtitle = models.CharField(max_length=255, blank=True, null=True)
    intro = RichTextField(blank=True)
    body = StreamField([
        ('paragraph', SimpleRichTextBlock()),
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
    search_fields = Page.search_fields + (
        index.SearchField('intro'),
        index.SearchField('body'),
        index.SearchField('subtitle'),
    )

    @property
    def pages(self):
        # Get list of live comp pages that are descendants of this page
        return SimplePage.objects.live().descendant_of(self)


SimplePage.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('subtitle', classname="full"),
    FieldPanel('intro', classname="full"),
    StreamFieldPanel('body'),
]

SimplePage.promote_panels = Page.promote_panels + [
    ImageChooserPanel('feed_image'),
]
