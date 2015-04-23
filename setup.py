from setuptools import setup,find_packages


setup(
    name='django-simplecrud',

    version='1.0b11',
    description='CRUD framework for Django',
    long_description="A simple Create-Review-Update-Delete framework for Django. Ready to use out-of-the-box: includes both views and templates",
    keywords='django, crud, views, templates',
    author='Pedro Tavares',
    author_email='pedro@ermapp.net',
    url='https://github.com/ptav/django-simplecrud',
    license='LICENSE',

    packages=find_packages(),
    
    include_package_data=True,
    zip_safe=False,
    
    install_requires=[
        #"Django >= 1.4.0",
        "six",
    ],
      
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Framework :: Django",
        "Environment :: Web Environment",
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
    ],
)
