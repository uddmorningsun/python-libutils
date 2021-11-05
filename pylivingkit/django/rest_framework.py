import logging

from django.urls.resolvers import URLResolver, URLPattern


def clear_viewset_permission_classes(all_url_patterns):
    """Hacking drf ViewSet.permission_classes policy is always granted permissions access.

    In fact, it will do ViewSet.permission_classes = []
    drf permissions: https://www.django-rest-framework.org/api-guide/permissions/
    """
    for url_pattern in all_url_patterns:  # type: URLPattern
        if isinstance(url_pattern, URLResolver):
            clear_viewset_permission_classes(url_pattern.url_patterns)
            continue
        callback, lookup_str = url_pattern.callback, url_pattern.lookup_str
        # FIXME: more elegant method
        if not hasattr(url_pattern.callback, "cls"):
            logging.info("skip (%s:%s) since not find 'cls' attr" % (callback, lookup_str))
            continue
        permission_classes = url_pattern.callback.cls.permission_classes
        if permission_classes:
            logging.info(
                "replace (%s:%s) permission_classes=%s to []" % (callback, lookup_str, permission_classes)
            )
            url_pattern.callback.cls.permission_classes = []
