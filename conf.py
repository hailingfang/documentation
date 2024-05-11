# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "Benjamin Fang's Docs"
copyright = '2023-2024, Benjamin Fang'
author = 'Benjamin Fang'
release = '0.2.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ["myst_parser", "sphinx_book_theme", "sphinx.ext.mathjax"]

templates_path = ['_templates']
html_static_path = ['_static']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', 'README.rst', 'file-format/README.rst']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

#using rtd theme and modify it's settings
html_theme = 'sphinx_book_theme'
html_theme_options = {
    "repository_url": "https://github.com/benjaminfang/documentation",
    "use_repository_button": True,
    'analytics_id': 'G-VWP9HESP22'
}

#change the logo
github_url = "https://github.com/benjaminfang/documentation"
html_logo = "img/doc-logo.svg"
html_title = "My site title"


# Add Google Analytics tracking code
html_js_files = ['https://www.googletagmanager.com/gtag/js?id=G-VWP9HESP22']
html_js_body = """
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'YOUR_TRACKING_ID');
</script>
"""

