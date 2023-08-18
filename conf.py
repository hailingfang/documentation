# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "Benjamin Fang's Docs"
copyright = '2023, Benjamin Fang'
author = 'Benjamin Fang'
release = '0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ["myst_parser", "sphinx_rtd_theme", "sphinx.ext.mathjax"]

templates_path = ['_templates']
html_static_path = ['_static']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', 'README.rst', 'file-format/README.rst']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

#using rtd theme and modify it's settings
html_theme = 'sphinx_rtd_theme'
html_theme_options = {
    "analytics_id" : None,
    "logo_only" : True,
    "display_version" : True
}

#change the logo
github_url = "https://github.com/benjaminfang/documentation"
html_logo = "img/BF-doc-logo.svg"
