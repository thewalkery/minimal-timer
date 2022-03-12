from codecs import open as codecs_open
from setuptools import setup, find_packages


# Get the long description from the relevant file
with codecs_open('README.rst', encoding='utf-8') as f:
    long_description = f.read()


setup(name='Minimal Timer',
      version='1.0',
      description=u"Minimal Timer Application",
      long_description=long_description,
      classifiers=[],
      keywords='',
      author=u"The Walker",
      author_email='thewalkery74@gmail.com',
      url='https://github.com/thewalkery/minimal-timer',
      license='LGPL',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          #'click'
      ],
      extras_require={
          #'test': ['pytest'],
      },
      entry_points=""""""
      #"""
      #[console_scripts]
      #pyskel=pyskel.scripts.cli:cli
      #"""
      )