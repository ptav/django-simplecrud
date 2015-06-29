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
    
You can then access this in a template. For example: `{{ simplecrud.message }}`

The following settings have a particular meaning when using SIMPLECRUD:

container   Top level class (default is `container`). For example, to switch
            to a full width container set it this parameter to 
            `container-fluid`.
                
                

### ListView

the `ListView` class is very flexible and allows one to design complex pages
from within Python. the key step is the `get_object_list` function. Here is a 
first simple example (more to follow later):

```python
import simplecrud


class HomeView(simplecrud.ListView):
	template_title = ''
	widget = 'simplecrud/widget/list.html'
	attributes = {
	    'links': None, # removes default model create and edit links
	}
	
	def get_object_list(self):
	    top = {
	        'widget': 'simplecrud/widget/text.html',
	        'object_list': [
	            '<h1 class="text-center">This is my website</h1><br><br>',
	            '<a href="#scroll2">',
	            '<h2 class="text-center">Find out more</h2>',
	            '</a>',
	        ],   
	        'attributes': {
	            'class':'jumbotron',
	        },
	    }
	    
	    mid = {
	        'widget': 'simplecrud/widget/text.html',
	        'object_list': [
	            '<a id="scroll2"></a>',
	            '<h3 class="text-center">Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.<h3>',
	            '<h3 class="text-center">Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.<h3>',
	            '<h3 class="text-center">Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.<h3>',
	        ],
	        'attributes': {
	            'class':'jumbotron',
	        },
	    }
	
	    bot = {
	        'widget': 'simplecrud/widget/list.html',
	        'object_list': self._block_panels(),
	    }
	
	    return [top,mid,bot]
	
	
	def _block_panels(self):
	    left = {
	        'widget': 'simplecrud/widget/text.html',
	        'object_list': [
	            '<h1 class="text-center">First</h1>',
	            '<p class="text-center">Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.</p>',
	        ],   
	        'attributes': {
	            'class':'col-md-4',
	        },
	    }
	    
	    center = {
	        'widget': 'simplecrud/widget/text.html',
	        'object_list': [
	            '<h1 class="text-center">Second</h1>',
	            '<p class="text-center">Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.</p>',
	        ],   
	        'attributes': {
	            'class':'col-md-4',
	        },
	    }
	
	    right = {
	        'widget': 'simplecrud/widget/text.html',
	        'object_list': [
	            '<h1 class="text-center">Third</h1>',
	            '<p class="text-center">Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.</p>',
	        ],   
	        'attributes': {
	            'class':'col-md-4',
	        },
	    }
	
	    return [left,center,right]
```
