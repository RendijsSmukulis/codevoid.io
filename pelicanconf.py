#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Rendijs Smukulis'
SITENAME = 'Code Void'
SITEURL = ''

PATH = 'content'

TIMEZONE = 'Europe/London'

DEFAULT_LANG = 'English'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

DISPLAY_PAGES_ON_MENU = True

# Blogroll
LINKS = ()

# Social widget
SOCIAL = (('My GitHub', 'https://github.com/RendijsSmukulis'),
          )

DEFAULT_PAGINATION = 10

extra_icons = ['favicon.ico', 'android-chrome-192x192.png', 'android-chrome-256x256.png', 'apple-touch-icon.png', 'browserconfig.xml',  'favicon-16x16.png',  'favicon-32x32.png', 'manifest.json', 'mstile-150x150.png', 'safari-pinned-tab.svg']

STATIC_PATHS = ['images']
STATIC_PATHS.extend(list(map(lambda x: "extra/" + x, extra_icons)))
print(STATIC_PATHS)

EXTRA_PATH_METADATA = {}    	

for icon in extra_icons:
    EXTRA_PATH_METADATA["extra/" + icon] = {"path": icon}


# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
