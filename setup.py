import os

from setuptools import setup, find_packages

def read(fname):
	return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
	name = 'django-timesheet',
	version = '0.1',
	url = 'http://github.com/myles/django-timesheet',
	license = 'BSD License',
	description = 'A Django timesheet application.',
	long_description = read('README'),
	
	author = 'Myles Braithwaite',
	author_email = 'me@mylesbraithwaite.com',
	
	packages = find_packages('src'),
	package_dir = {'': 'src'},
	
	install_requires = [
		'setuptools',
		'python-dateutil',
	],
	
	classifiers = [
		'Development Status :: 4 - Beta',
		'Framework :: Django',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: BSD License',
		'Operating System :: OS Independent',
		'Programming Language :: Python',
		'Topic :: Internet :: WWW/HTTP',
	],
)
