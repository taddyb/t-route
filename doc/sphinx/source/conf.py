# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'T-Route'
copyright = '2024, NOAA-OWP'
author = 'DongHa Kim, Sean Horvath, Amin Torabi, Zach Jurgen'
# release = '2.4.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "numpydoc",
    "sphinx_design",
    "sphinx.ext.autosummary",
    "sphinx.ext.viewcode", 
    "sphinx.ext.githubpages",
    "sphinx_mdinclude",
]

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# html_sidebars = {
#     "index": ["search-button-field"],
#     "**": ["search-button-field", "sidebar-nav-bs"]
# }

html_theme = 'pydata_sphinx_theme'
html_theme_options = {
    "github_url": "https://github.com/NOAA-OWP/t-route",
    "use_edit_page_button": True,
    "show_toc_level": 1,
    "navbar_align": "left",  # [left, content, right] For testing that the navbar items align properly
    # "show_nav_level": 2,
    "navbar_center": ["navbar-nav"],
    "secondary_sidebar_items": {
        "**/*": ["page-toc", "sourcelink"],
        "examples/no-sidebar": [],
    },
}
html_css_files = [
    "css/custom.css",
]
html_static_path = ['_static']
