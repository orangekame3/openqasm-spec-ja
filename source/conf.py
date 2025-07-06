#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
OpenQASM Japanese Translation Documentation Configuration
"""

import os
import sys
import datetime

# Build paths
sys.path.insert(0, os.path.abspath('.'))
sys.path.insert(0, os.path.abspath('_extensions'))

# Project information
project = 'OpenQASM 3.0 仕様書'
copyright = f'2017-{datetime.datetime.now().year}, OpenQASM Contributors'
author = 'OpenQASM Contributors'

# Version information
version = '3.0'
release = '3.0'

# General configuration
source_suffix = '.rst'
master_doc = 'index'
language = 'ja'
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
pygments_style = 'sphinx'
highlight_language = 'qasm3'

# Extensions
extensions = [
    'sphinx.ext.mathjax',
    'sphinx.ext.githubpages',
    'sphinxcontrib.bibtex',
]

# Bibliography configuration
bibtex_bibfiles = ['bibliography.bib']

# HTML output options
html_theme = 'alabaster'
html_static_path = ['_static']
html_title = f'{project} {version}'
html_short_title = 'OpenQASM 3.0 仕様書'

# GitHub Pages configuration
html_baseurl = 'https://orangekame3.github.io/openqasm-spec-ja/'
html_context = {
    'display_github': True,
    'github_user': 'orangekame3',
    'github_repo': 'openqasm-spec-ja',
    'github_version': 'main',
    'conf_py_path': '/source/',
}

# Theme options
html_theme_options = {
    'description': 'OpenQASM 3.0 仕様書 日本語版',
    'github_user': 'orangekame3',
    'github_repo': 'openqasm-spec-ja',
    'github_button': True,
    'github_banner': True,
    'github_type': 'star',
    'fixed_sidebar': True,
    'sidebar_width': '200px',
    'page_width': '1000px',
}

# Additional sidebar templates
html_sidebars = {
    '**': [
        'about.html',
        'navigation.html',
        'relations.html',
        'searchbox.html',
        'donate.html',
    ]
}

# LaTeX output options
latex_elements = {
    'papersize': 'a4paper',
    'pointsize': '10pt',
    'preamble': r'''
\usepackage{xeCJK}
\setCJKmainfont{Noto Sans CJK JP}
\setCJKsansfont{Noto Sans CJK JP}
\setCJKmonofont{Noto Sans Mono CJK JP}
''',
}

latex_documents = [
    (master_doc, 'openqasm-spec-ja.tex', project, author, 'manual'),
]

# Internationalization
gettext_compact = False
locale_dirs = ['_locale']

# Figure numbering
numfig = True
numfig_format = {
    'figure': '図 %s',
    'table': '表 %s',
    'code-block': 'リスト %s',
}

# Math support
mathjax_path = 'https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js'
mathjax3_config = {
    'tex': {
        'inlineMath': [['$', '$'], ['\\(', '\\)']],
        'displayMath': [['$$', '$$'], ['\\[', '\\]']],
    }
}