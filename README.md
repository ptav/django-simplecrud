django-simplecrud
=================

Create-Review-Update-Delete view and template framework for Django


Installation
------------

From the top directory of django-crud, run `setup.py install` 


Usage
-----

1. Add `'crud'` to `INSTALLED_APPS`

2. Define CRUD_SETTINGS in your Django project `settings.py` file. The variable 
is a dictionary that sets certain  parameters for the navbar and footer of the 
web pages generated: 

	`navbar_logo`	is a HTML safe string detailing the logo to use in the navbar
	`navbar_menu`	is also an HTML safe string detailing the Bootstrap3 navbar menu options
	`copyright`		a message added to the footer

	For example:

	```python
	CRUD_SETTINGS = {
	    'navbar_logo':  '<b><i>my</i>Logo</b>',
	    'navbar_menu':  '<li class="active"><a href="/">Home</a></li>',
	    'copyright':    'Copyright (c) 2015',
	}
	```

3. Add the URL patterns to the models you wish to access through the CRUD library.
For example:

	in the main `urls.py`

	```python
	urlpatterns = patterns('',
		...
		
	    url(r'^mymodel/', include('mymodel.urls') ),
	
		...
	)
	```

	Then in `mymodel/urls.py`

	```python
	import crud
	from .models import MyModel
	
	url_patters = crud.urls(MyModel)
	```
	
	This will create a series of URLs:
	
	```
	/mymodel/create
	/mymodel/update
	/mymodel/delete
	/mymodel/list
	/mymodel/formset
	```

	The `urls` function accepts other parameters such as the forms to be 
	used for create and update, queryset for list and formset and redirect 
	URL for succesful use of create, update, delete and formset

4. Each view accepts a series of options that customise their behaviour. Until
the documentation is expanded, please inspect the code for instructions. The 
default behaviour of the views will be a good guide to how these can be changed 
until better documentation becomes available.

