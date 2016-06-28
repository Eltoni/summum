#-*- coding: UTF-8 -*-
class TagAlreadyRegistered(Exception):
    "Exception when trying to register a tag which is already registered."


class TagNotRegistered(Exception):
    "Exception when trying use a tag which is not registered."


class TagInvalid(Exception):
    "Exception when register an invalid tag class."