import os
from setuptools import setup, find_packages

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

requirements = open(os.path.join(os.path.dirname(__file__),
            'requirements.txt')).read()
requires = requirements.strip().split('\n')

extra_requirements = open(os.path.join(os.path.dirname(__file__),
            'requirements-testing.txt')).read()
extra_requires = extra_requirements.strip().split('\n')
if not isinstance(extra_requires, list):
    print("requirements-testing.txt was not parsed correctly.")
    extra_requires = []


setup(
    name='threatingestor',
    version='1.0.2',
    include_package_data=True,
    install_requires=requires,
    extras_require={
        'twitter': ['twitter'],
        'rss': ['feedparser'],
        'misp': ['PyMISP'],
        'threatkb': ['threatkb'],
        'beanstalk': ['greenstalk'],
        'sqs': ['boto3'],
        'mysql': ['pymysql'],
        'extras': ['hug', 'boto3', 'greenstalk', 'watchdog'],
        'all': extra_requires,
    },
    entry_points={
          'console_scripts': [
              'threatingestor = threatingestor:main'
          ]
    },
    license='GPL',
    description='Extract and aggregate IOCs from threat feeds.',
    long_description=README,
    url='https://github.com/InQuest/ThreatIngestor',
    author='InQuest Labs',
    author_email='labs@inquest.net',
    packages=find_packages(),
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Security',
        'Topic :: Internet',
    ],
)
