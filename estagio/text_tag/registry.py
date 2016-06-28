#-*- coding: UTF-8 -*-
from __future__ import unicode_literals
from django.utils.encoding import force_text
from django.utils.module_loading import autodiscover_modules
import re

from text_tag.exceptions import TagAlreadyRegistered


class TagRegistry(object):

    def __init__(self):
        self._registry = {}

    def register(self, tag):
        # self.validate(tag)
        found_tags = [k for k,v in tag.__dict__.items() if k.endswith('_tag') or k.endswith('_filter')]
        for i in found_tags:
            if i in self._registry:
                raise TagAlreadyRegistered('The name %s is already registered' % i)
            self._registry[i] = getattr(tag(), i)

    def unregister(self, tag):
        self.validate(tag)
        name = force_text(tag.name())
        if name not in self._registry:
           pass
           # raise LookupNotRegistered('The name %s is not registered' % name)
        del self._registry[name]

    @property
    def get_all_tag_registers(self):
        # print(list((k, v) for (k, v) in self._registry.items() if k.endswith('_tag')))
        return dict((k, v) for (k, v) in self._registry.items() if k.endswith('_tag'))

    @property
    def get_all_filter_registers(self):
        return dict((k, v) for (k, v) in self._registry.items() if k.endswith('_filter'))

    def get(self, key):
        return self._registry.get(key, None)


registry = TagRegistry()


def autodiscover():
    # Attempt to import the app's lookups module.
    autodiscover_modules('tags', register_to=registry)