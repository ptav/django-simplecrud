# django-simplecrud

Create-Review-Update-Delete view and template framework for Django


## Installation

Run `pip install django-simplecrud` for installing the latest stable release

You can also install a local copy by running `setup.py install` at the top
directory of django-simplecrud


## Usage

1. Add `'simplecrud'` to `INSTALLED_APPS`


2.  Overwrite Templates
    
    Any default template can be overwriten in the normal way: by creating a 
    folder in your project template directory (`templates/simplecrud`) and 
    copying the library templates. For example, you could copy the 
    `copyright.html`, `logo.html` and `menu.html` templates to setup your site's
    own copyright message, logo and navbar menu.


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


### SIMPLECRUD

You can define SIMPLECRUD in your Django project `settings.py` file. The variable 
will be passed to simplecrud templates in the context, inside the `simplecrud`
parameter 

    For example:

    ```python
    SIMPLECRUD = {
        'message': 'My message!',
    }
    ```
    
    You can then access this in a template. For example:
    
    ```
    {{ simplecrud.message }}
    ```

