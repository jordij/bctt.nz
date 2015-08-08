from wagtail.wagtailcore.blocks import StructBlock, RichTextBlock
from wagtail.wagtailsnippets.blocks import SnippetChooserBlock
from wagtail.wagtailcore.blocks import DateBlock, StreamBlock, ListBlock

from .snippets import Team


class GameBlock(StructBlock):
    first_team = SnippetChooserBlock(Team, required=True)
    second_team = SnippetChooserBlock(Team, required=True)
    results = RichTextBlock(required=False)

    class Meta:
        icon = 'spinner'
        form_classname = 'game-block struct-block'


class CompDayBlock(StreamBlock):
    date = DateBlock(required=True)
    games = ListBlock(GameBlock())

    class Meta:
        icon = 'group'
