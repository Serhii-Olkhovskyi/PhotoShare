import sys
import os


sys.path.append(os.path.abspath('..'))

project = 'PhotoShare'
copyright = '2023, Redis_K@'
author = 'Redis_K@'

extensions = ['sphinx.ext.autodoc']

templates_path = ['_templates']
exclude_patterns = []

html_theme = 'nature'
html_static_path = ['_static']
