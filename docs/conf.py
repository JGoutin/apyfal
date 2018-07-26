# -*- coding: utf-8 -*-
"""Sphinx documentation """

# -- Path setup --------------------------------------------------------------

import os
from os.path import abspath, dirname, join, isdir
from subprocess import check_output
import sys

SETUP_PATH = abspath(dirname(dirname(__file__)))
sys.path.insert(0, SETUP_PATH)


# -- Get information from setup.py -------------------------------------------

# Get Package info
from setup import PACKAGE_INFO, REST_API_DST
SPHINX_INFO = PACKAGE_INFO['command_options']['build_sphinx']


# -- Prepare environment for ReadTheDocs -------------------------------------

if os.environ.get('READTHEDOCS'):
    # Install dependencies
    from subprocess import Popen
    current_dir = os.getcwd()
    os.chdir(SETUP_PATH)
    try:
        Popen('python -m pip install -e .[all]', shell=True).communicate()
    finally:
        os.chdir(current_dir)

    # Mock apyfal.client.rest._openapi since Java not available on ReadTheDocs
    try:
        os.makedirs(REST_API_DST)
    except OSError:
        if not isdir(REST_API_DST):
            raise
    with open(join(REST_API_DST, '__init__.py'), 'wt') as rest_init:
        rest_init.write('')


# -- Dynamically generates documentation for "accelerator.conf" file ----------


def _generates_rst(rst_path, content):
    """
    Generates a reStructuredText file with specified content.

    Args:
        rst_path (str): Path to ".rst" file
        content (list of str): File content lines.
    """
    with open(rst_path, 'wt', encoding='utf-8') as rst_file:
        rst_file.write('\n'.join(
            [".. WARNING:\n   This file is autogenerated"
             ", do not edit it manually\n"] + content))


def rst_from_conf(conf_path, rst_path):
    """
    Generate a reStructuredText file from a properly
    formatted ".conf" file.

    ".conf" file needs to use ";" as comment symbol.
    Comments can be written in reStructuredText format.

    Args:
        conf_path (str): Path to ".conf" file.
        rst_path (str): Path to ".rst" file
    """
    # Read ".conf"
    with open(conf_path, 'rt', encoding='utf-8') as conf_file:
        content = conf_file.readlines()

    # Convert to markdown
    for index, line in enumerate(content):
        line = line.rstrip()

        # Skip blank lines
        if not line:
            pass

        # Remove comments marks
        elif line.startswith(';'):
            line = line.lstrip(';')

        # Remove [] from section
        elif line.startswith('['):
            line = 'The "%s" section' % line.strip('[]')

        # Quote parameters lines
        else:
            line = '``%s``' % line

        content[index] = line

    # Save ".rst"
    _generates_rst(rst_path, content)


rst_from_conf('../apyfal/accelerator.conf', 'configuration_file.rst')


# -- Dynamically generates documentation from Apyfal CLI help ----------

def generates_cli_help(rst_path):
    """
    Generate a reStructuredText file from Apyfal CLI '--help' commands.

    Args:
        rst_path (str): Path to ".rst" file
    """
    cli = [sys.executable or 'python', '../apyfal/__main__.py']
    commands = ('', 'create', 'start', 'process', 'stop', 'copy', 'clear')
    content = [
        'Apyfal CLI help',
        '===============\n',
        'This section provides full CLI help (from ``--help``)',
        'for each command.\n']

    for command in commands:
        help = check_output(
            cli + ([command, '-h'] if command else ['-h']), universal_newlines=True)
        title = 'apyfal%s' % ((' %s' % command) if command else '')
        content += [
            title, '-' * len(title), '\n| ' + help.replace('\n', '\n| '), '']

    # Save ".rst"
    _generates_rst(rst_path, content)


generates_cli_help('cli_help.rst')


# -- Project information -----------------------------------------------------

project = SPHINX_INFO['project'][1]
copyright = SPHINX_INFO['copyright'][1]
author = PACKAGE_INFO['author']
version = SPHINX_INFO['version'][1]
release = SPHINX_INFO['release'][1]


# -- General configuration ---------------------------------------------------

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.napoleon',
              'sphinx.ext.coverage', 'sphinx.ext.viewcode']
source_suffix = '.rst'
master_doc = 'index'
language = 'en'
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
pygments_style = 'default'


# -- Options for HTML output -------------------------------------------------

html_theme = 'sphinx_rtd_theme'


# -- Options for HTMLHelp output ---------------------------------------------

htmlhelp_basename = '%sdoc' % project


# -- Options for LaTeX output ------------------------------------------------

latex_elements = {}
latex_documents = [(
    master_doc, '%s.tex' % project, '%s Documentation' % project, author,
    'manual')]


# -- Options for manual page output ------------------------------------------

man_pages = [(
    master_doc, PACKAGE_INFO['name'], '%s Documentation' % project,
    [author], 1)]


# -- Options for Texinfo output ----------------------------------------------

texinfo_documents = [(
    master_doc, project, '%s Documentation' % project, author, project,
    PACKAGE_INFO['description'], 'Miscellaneous')]
