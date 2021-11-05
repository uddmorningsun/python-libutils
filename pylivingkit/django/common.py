import typing

from django.conf import settings
from django.urls.resolvers import get_resolver, URLResolver, URLPattern

ADMIN_URLRESOLVER = "admin:admin"


def get_urlpath2viewfunction_mapping(
    include_admin_site=False, *, urlpath_to_viewfunction=None
) -> typing.Dict[str, typing.Dict]:
    result_mapping = {}
    all_url_patterns = get_resolver(settings.ROOT_URLCONF).url_patterns

    def _urlpath_to_viewfunction(url_patterns: typing.List[typing.Union[URLPattern, URLResolver]]):
        for i in url_patterns:
            if isinstance(i, URLResolver):
                if "%s:%s" % (i.app_name, i.namespace) == ADMIN_URLRESOLVER and not include_admin_site:
                    continue
                urlpath_to_viewfunction(i.url_patterns)
                # If not clause, subelement recursive function gets result and will run continuely, it should be break :)
                continue
            result_mapping["%s -- %s" % (i.pattern, i.pattern.name)] = {
                "viewFunc": {"endPoint": i.lookup_str, "name": i.name, "callback": i.callback.__name__},
                "describe": i.pattern.describe(),
            }

    if urlpath_to_viewfunction is not None and not callable(urlpath_to_viewfunction):
        raise TypeError("{!r} is not a callable object".format(urlpath_to_viewfunction))
    if urlpath_to_viewfunction is None:
        urlpath_to_viewfunction = _urlpath_to_viewfunction
    urlpath_to_viewfunction(all_url_patterns)
    return result_mapping
