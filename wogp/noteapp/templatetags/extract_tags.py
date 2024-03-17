from django import template

register = template.Library()


def tags(note_tags):
    return ', '.join([f'{tag}' for tag in note_tags.all()])


register.filter('tags', tags)
