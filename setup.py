from setuptools import setup, find_packages

version = '0.1'

setup(name='affinitic.imageuploader',
      version=version,
      description="",
      long_description=open("README.md").read(),
      # Get more strings from https://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
          "Topic :: Software Development :: Libraries :: Python Modules",
          "Programming Language :: Python",
          "Framework :: Plone",
      ],
      keywords='',
      author='Affinitic',
      author_email='info@affinitic.be',
      url='https://github.com/affinitic/affinitic.imageuploader',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['affinitic'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'Products.LocalFS',
          ],
      extras_require=dict(
          scripts=[]),
      entry_points={}
      )
