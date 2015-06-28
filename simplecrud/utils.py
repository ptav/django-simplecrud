from __future__ import unicode_literals

#from django.core.exceptions import ImproperlyConfigured
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse,reverse_lazy
from django.http import  QueryDict,Http404


"""
==============
CRUD framework
==============

Copyright (c) 2015 Pedro Tavares, All rights reserved

General utilities used in simplecrud

"""


def render_glyphicon(name):
    "Render glyphicon `name`"
    return mark_safe('<span class="glyphicon glyphicon-{0}"></span>'.format(name))




def reverse_with_query(named_url,**kwargs):
    "Reverse named URL with GET query"
    q = QueryDict('',mutable=True)
    q.update(kwargs)
    return '{}?{}'.format(reverse(named_url),q.urlencode()) 




def reverse_lazy_with_query(named_url,**kwargs):
    "Reverse named URL with GET query (lazy version)"
    q = QueryDict('',mutable=True)
    q.update(kwargs)
    return '{}?{}'.format(reverse_lazy(named_url),q.urlencode()) 




def urls(model,form_class=None,fields=None,redirect=None,object_list=None,fail_if_empty=True):
    """
    Returns URL patterns for creating, updating and deleting models. Supports lists and formsets as well
    
    model          Model class
    form_class     Form class for use in create, update and formset views (default is None)
    fields         Required if form_class is not provided
    redirect       Redirection URL for create, update and delete views
    object_list    Queryset for list and formset. If absent, these views are not created
    fail_if_empty  Raise ImproperlyConfigured exception in formset and list views when object_list is empty
    """
    
    if form_class is None and fields is None:
        raise ImproperlyConfigured("Must define either `form_class` or `fields`.")
    
    if object_list is None and redirect is None:
        raise ImproperlyConfigured("Must define `redirect` when `object_list` is missing.")
    
    prefix = model.__name__.lower()
    if redirect is None: redirect = reverse_lazy(prefix + '_list')
    
    urlpatterns = patterns('',
        # Create a new record
        url('^' + prefix + '/create/',
            CreateView.as_view(model=model,form_class=form_class,fields=fields,success_url=redirect),
            name = prefix + '_create'
        ),
                            
        # Update record 'pk'
        url('^' + prefix + '/update/(?P<pk>\d+)/',
            UpdateView.as_view(model=model,form_class=form_class,fields=fields,success_url=redirect),
            name = prefix + '_update'
        ),
        
        # Delete record 'pk'
        url('^' + prefix + '/delete/(?P<pk>\d+)/',
            DeleteView.as_view(model=model,success_url=redirect),
            name = prefix + '_delete'
        ),                            
    )
    
    if object_list:
        urlpatterns += patterns('',
            # List records
            url('^' + prefix + '/list/',
                ListView.as_view(model=model,object_list=object_list,fail_if_empty=fail_if_empty),
                name = prefix + '_list'
            ),
                                
            # Edit records using a formset
            url('^' + prefix + '/formset/',
                FormsetView.as_view(model=model,form_class=form_class,fields=fields,object_list=object_list,fail_if_empty=fail_if_empty),
                name = prefix + '_formset'
            ),
        )

    
    return urlpatterns
