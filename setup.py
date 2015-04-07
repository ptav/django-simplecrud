from setuptools import setup,find_packages

    
setup(
    name='django-simplecrud',

    version='0.1',
    description='CRUD framework for Django',
    keywords='django crud',
    author='Pedro Tavares',
    author_email='pedro@ermapp.net',
    url='https://github.com/ptav/django-crud',
    license='LICENSE',

    packages=find_packages(),
    
    include_package_data=True,

    #install_requires=[
    #    "Django >= 1.4.0"
    #],
)
