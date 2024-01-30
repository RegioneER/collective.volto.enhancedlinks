"""Installer for the collective.volto.enhancedlinks package."""

from setuptools import find_packages
from setuptools import setup


long_description = "\n\n".join(
    [
        open("README.rst").read(),
        open("CONTRIBUTORS.rst").read(),
        open("CHANGES.rst").read(),
    ]
)


setup(
    name="collective.volto.enhancedlinks",
    version="1.0.1",
    description="Enhance Volto text blocks to automatically append file size and mimetype to internal links",
    long_description=long_description,
    # Get more from https://pypi.org/classifiers/
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: Addon",
        "Framework :: Plone :: 5.2",
        "Framework :: Plone :: 6.0",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
    keywords="Python Plone CMS",
    author="RedTurtle Technology",
    author_email="sviluppo@redturtle.it",
    url="https://github.com/collective/collective.volto.enhancedlinks",
    project_urls={
        "PyPI": "https://pypi.org/project/collective.volto.enhancedlinks/",
        "Source": "https://github.com/collective/collective.volto.enhancedlinks",
        "Tracker": "https://github.com/collective/collective.volto.enhancedlinks/issues",
        # 'Documentation': 'https://collective.volto.enhancedlinks.readthedocs.io/en/latest/',
    },
    license="GPL version 2",
    packages=find_packages("src", exclude=["ez_setup"]),
    namespace_packages=["collective", "collective.volto"],
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.8",
    install_requires=["setuptools", "plone.volto"],
    extras_require={
        "test": [
            "gocept.pytestlayer",
            "plone.app.testing",
            "plone.restapi[test]",
            "pytest-cov",
            "pytest-plone>=0.2.0",
            "pytest-docker",
            "pytest-mock",
            "pytest",
            "zest.releaser[recommended]",
            "zestreleaser.towncrier",
            "pytest-mock",
            "requests-mock",
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    [console_scripts]
    update_locale = collective.volto.enhancedlinks.locales.update:update_locale
    """,
)
