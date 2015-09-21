"""
Map interface page for displaying user locations.
"""

from django.http import HttpResponse
from django.template import RequestContext, loader


def index(request):
    """
    Render a page containing a map with the public
    user locations available.

    Allow zoom, pan, and clicking for more info.
    """
    template = loader.get_template('api/map.html')
    context = RequestContext(request, {})
    return HttpResponse(template.render(context))
