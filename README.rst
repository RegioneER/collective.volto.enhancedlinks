.. This README is meant for consumption by humans and PyPI. PyPI can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on PyPI or github. It is a comment.

.. image:: https://github.com/collective/collective.volto.enhancedlinks/actions/workflows/plone-package.yml/badge.svg
    :target: https://github.com/collective/collective.volto.enhancedlinks/actions/workflows/plone-package.yml

.. image:: https://coveralls.io/repos/github/collective/collective.volto.enhancedlinks/badge.svg?branch=main
    :target: https://coveralls.io/github/collective/collective.volto.enhancedlinks?branch=main
    :alt: Coveralls

.. image:: https://codecov.io/gh/collective/collective.volto.enhancedlinks/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/collective/collective.volto.enhancedlinks

.. image:: https://img.shields.io/pypi/v/collective.volto.enhancedlinks.svg
    :target: https://pypi.python.org/pypi/collective.volto.enhancedlinks/
    :alt: Latest Version

.. image:: https://img.shields.io/pypi/status/collective.volto.enhancedlinks.svg
    :target: https://pypi.python.org/pypi/collective.volto.enhancedlinks
    :alt: Egg Status

.. image:: https://img.shields.io/pypi/pyversions/collective.volto.enhancedlinks.svg?style=plastic   :alt: Supported - Python Versions

.. image:: https://img.shields.io/pypi/l/collective.volto.enhancedlinks.svg
    :target: https://pypi.python.org/pypi/collective.volto.enhancedlinks/
    :alt: License


==============================
collective.volto.enhancedlinks
==============================

Enhance Volto slate blocks to automatically append file size and mimetype to internal links.

Features
--------

When you link a content in slate block, if the linked object has `volto.enhanced_links_enabled` behavior enabled,
an extra data will be appended to the block with its size and mimetype.

By default the behavior is enabled for:

- File
- Image


Installation
------------

Install collective.volto.enhancedlinks by adding it to your buildout::

    [buildout]

    ...

    eggs =
        collective.volto.enhancedlinks


and then running ``bin/buildout``


Contribute
----------

- Issue Tracker: https://github.com/RegioneEr/collective.volto.enhancedlinks/issues
- Source Code: https://github.com/RegioneEr/collective.volto.enhancedlinks


Compatibility
-------------

This product has been tested on:

* Plone 6


License
-------

The project is licensed under the GPLv2.


Credits
-------

Developed with the support of:

* `Regione Emilia Romagna`__


Regione Emilia-Romagna supports the `PloneGov initiative`__.

__ http://www.regione.emilia-romagna.it/
__ http://www.plonegov.it/


Authors
-------

This product was developed by RedTurtle Technology team.

.. image:: http://www.redturtle.it/redturtle_banner.png
   :alt: RedTurtle Technology Site
   :target: http://www.redturtle.it/
