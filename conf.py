# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "Hailing Fang's Docs"
copyright = '2023-2025, Hailing Fang'
author = 'Hailing Fang'
release = '0.2.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ["myst_parser", "sphinx_book_theme", "sphinx.ext.mathjax"]

templates_path = ['_templates']
html_static_path = ['_static']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', 'README.rst', 'file-format/file-format/README.rst']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

#using rtd theme and modify it's settings
html_theme = 'sphinx_book_theme'
html_theme_options = {
    "repository_url": "https://github.com/hailingfang/documentation",
    "use_repository_button": True,
    #"navbar_start": ["home_nav.html"],

    "icon_links": [
        {
            "name": "Go Home",
            "url": "https://hailingfang.github.io",
            "icon": "_static/logo-fanghl.svg",
            "type": "local",
        },
    ],
}

#change the logo
html_logo = "_static/doc-logo.svg"
html_title = "Documentation | Hailing Fang"
html_favicon = 'favicon.png'


# Add Google Analytics tracking code
html_static_path = ["_static"]
html_js_files = ['https://www.googletagmanager.com/gtag/js?id=G-VWP9HESP22', 'google_analytics.js']

