from setuptools import setup, find_packages

setup(name='turbine',
	  version='0.1',
	  description='A lightweight framework for receiving tweets from the Twitter streaming API.',

	  packages=find_packages(),
	  test_suite='nose.collector')