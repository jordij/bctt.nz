from django.db import models
import django.db.models.options as options
from django.db.models import Sum

from wagtail.wagtailadmin.edit_handlers import InlinePanel, FieldPanel, MultiFieldPanel, PageChooserPanel
from wagtail.wagtaildocs.edit_handlers import DocumentChooserPanel
from wagtail.wagtailsnippets.models import register_snippet
from wagtail.wagtailcore.models import Orderable
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel

from modelcluster.fields import ParentalKey

from .utilities import *
from .snippets import *

options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('description',)


class LinkFields(models.Model):

    """
    Represents a link to an external page, a document or a fellow page
    """
    link_external = models.URLField(
        "External link",
        blank=True,
        null=True,
        help_text='Set an external link if you want the link to point somewhere outside the CMS.'
    )
    link_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        on_delete=models.SET_NULL,
        blank=True,
        related_name='+',
        help_text='Choose an existing page if you want the link to point somewhere inside the CMS.'
    )
    link_document = models.ForeignKey(
        'wagtaildocs.Document',
        null=True,
        on_delete=models.SET_NULL,
        blank=True,
        related_name='+',
        help_text='Choose an existing document if you want the link to open a document.'
    )
    link_email = models.EmailField(
        blank=True,
        null=True,
        help_text='Set the recipient email address if you want the link to send an email.'
    )
    link_phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text='Set the number if you want the link to dial a phone number.'
    )

    @property
    def link(self):
        if self.link_page:
            return self.link_page.url
        elif self.link_external:
            return self.link_external
        elif self.link_document:
            return self.link_document.url
        elif self.link_email:
            return 'mailto:%s' % self.link_email
        elif self.link_phone:
            return 'tel:%s' % self.link_phone.strip()
        else:
            return "#"

    panels = [
        MultiFieldPanel([
            PageChooserPanel('link_page'),
            FieldPanel('link_external'),
            DocumentChooserPanel('link_document'),
            FieldPanel('link_email'),
            FieldPanel('link_phone'),
            ],
            "Link"
        ),
    ]

    class Meta:
        abstract = True


class MenuElement(LinkFields):
    explicit_name = models.CharField(
        max_length=64,
        blank=True,
        null=True,
        help_text='If you want a different name than the page title.'
    )
    short_name = models.CharField(
        max_length=32,
        blank=True,
        null=True,
        help_text='If you need a custom name for responsive devices.'
    )
    css_class = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="CSS Class",
        help_text="Optional styling for the menu item"
    )
    icon_class = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Icon Class",
        help_text="In case you need an icon element <i> for the menu item"
    )

    @property
    def title(self):
        if self.explicit_name:
            return self.explicit_name
        elif self.link_page:
            return self.link_page.title
        elif self.link_document:
            return self.link_document.title
        else:
            return None

    @property
    def url(self):
        return self.link

    def __unicode__(self):
        if self.explicit_name:
            title = self.explicit_name
        elif self.link_page:
            title = self.link_page.title
        else:
            title = ''
        return "%s ( %s )" % (title, self.short_name)

    class Meta:
        verbose_name = "Menu item"
        description = "Elements appearing in the main menu"

    panels = LinkFields.panels + [
        FieldPanel('explicit_name'),
        FieldPanel('short_name'),
        FieldPanel('css_class'),
        FieldPanel('icon_class'),
    ]


class NavigationMenuMenuElement(Orderable, MenuElement):
    parent = ParentalKey(to='NavigationMenu', related_name='menu_items')


class NavigationMenuManager(models.Manager):

    def get_by_natural_key(self, name):
        return self.get(menu_name=name)


@register_snippet
class NavigationMenu(models.Model):

    objects = NavigationMenuManager()
    menu_name = models.CharField(max_length=255, null=False, blank=False)

    @property
    def items(self):
        return self.menu_items.all()

    def __unicode__(self):
        return self.menu_name

    class Meta:
        verbose_name = "Navigation menu"
        description = "Navigation menu"


NavigationMenu.panels = [
    FieldPanel('menu_name', classname='full title'),
    InlinePanel('menu_items', label="Menu Items", help_text='Set the menu items for the current menu.')
]


@register_snippet
class Author(models.Model):

    """
    Short bio and profile pic for an author
    """
    name = models.CharField(max_length=255, blank=False)
    title = models.CharField(max_length=255, blank=True)
    bio = models.TextField(blank=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    class Meta:
        verbose_name = "Author Biography"
        verbose_name_plural = "Author Biographies"
        description = "Articles authors short bio"

    def __unicode__(self):
        return self.name

    panels = [
        FieldPanel('name'),
        FieldPanel('title'),
        FieldPanel('bio'),
        ImageChooserPanel('image'),
    ]


class Player(models.Model):

    """
    Short bio and profile pic for a player
    """
    name = models.CharField(max_length=255, blank=False)
    title = models.CharField(max_length=255, blank=True)
    bio = models.TextField(blank=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    class Meta:
        verbose_name = "Player profile"
        description = "Player profile"

    def __unicode__(self):
        return self.name

    panels = [
        FieldPanel('name'),
        FieldPanel('title'),
        FieldPanel('bio'),
        ImageChooserPanel('image'),
    ]


class TeamPlayer(Orderable, Player):
    parent = ParentalKey(to='Team', related_name='players')


class TeamManager(models.Manager):

    def get_by_natural_key(self, name):
        return self.get(menu_name=name)


@register_snippet
class Team(models.Model):

    """
    Team for player
    """
    name = models.CharField(max_length=255, blank=False)
    url = models.URLField(blank=True)
    bio = models.TextField(max_length=1020, blank=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    @property
    def get_wins(self):
        wins_one = self.competitions_as_one.all().annotate(Sum('team_one_games'))
        if wins_one['team_one_games__sum'] is None:
            wins_one['team_one_games__sum'] = 0
        wins_two = self.competitions_as_two.all().annotate(Sum('team_two_games'))
        if wins_two['team_two_games__sum'] is None:
            wins_two['team_two_games__sum'] = 0
        return wins_one['team_one_games__sum'] + wins_two['team_two_games__sum']

    @property
    def get_losts(self):
        wins_one = self.competitions_as_one.all().annotate(Sum('team_two_games'))
        if wins_one['team_two_games__sum'] is None:
            wins_one['team_two_games_sum'] = 0
        wins_two = self.competitions_as_two.all().annotate(Sum('team_one_games'))
        if wins_two['team_one_games__sum'] is None:
            wins_two['team_one_games__sum'] = 0
        return wins_one['team_one_games__sum'] + wins_two['team_two_games__sum']

    class Meta:
        verbose_name = "Team profile"
        description = "Team profile"

    def __unicode__(self):
        return self.name

    panels = [
        FieldPanel('name'),
        FieldPanel('url'),
        FieldPanel('bio'),
        ImageChooserPanel('image'),
        InlinePanel('players', label="Players", help_text='Set the players for this team.')
    ]


@register_snippet
class Sponsor(models.Model):

    """
    Team for player
    """
    name = models.CharField(max_length=255, blank=False)
    url = models.URLField(blank=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    class Meta:
        verbose_name = "Sponsor profile"
        description = "Business class sponsor"

    def __unicode__(self):
        return self.name

    panels = [
        FieldPanel('name'),
        FieldPanel('url'),
        ImageChooserPanel('image'),
    ]
