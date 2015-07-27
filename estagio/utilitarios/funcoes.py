#-*- coding: UTF-8 -*-
import xml.etree.ElementTree

def remove_tags(text):
    """Remove elementos html de uma string e retorna o resultado"""
    return ''.join(xml.etree.ElementTree.fromstring(text).itertext())
