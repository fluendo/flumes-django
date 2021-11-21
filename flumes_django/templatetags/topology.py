from django import template

register = template.Library()


@register.inclusion_tag("flume_django/templatetags/children.html")
def children_tag(stream):
    children = stream.children.all()
    return {"children": children}
