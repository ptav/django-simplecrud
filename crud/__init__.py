from __future__ import unicode_literals

import vanilla

from django.conf.urls import patterns,url
from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.forms.models import modelformset_factory
from django.shortcuts import redirect
from django.utils.safestring import mark_safe
from django.contrib import messages

try:
    from django.conf import settings
except ImportError as err:
    raise ImportError("Django project settings must define CRUD_SETTINGS")


# TODO: Edit, add and delete buttons are visible and active even if user has no modification/deletion rights to a model. Make these buttons sensitive to the setting


"""
==============
CRUD framework
==============

Copyright (c) 2015 Pedro Tavares, All rights reserved

The views that rely on forms (CreateView, UpdateView,FormsetView) add a new order argument to the get_form
function: the current request (from which the form can access certain data, such as the identity of the 
logged-in user)

Based on django-vanilla view library

"""


def render_glyphicon(name):
    "Render glyphicon 'name'"
    return mark_safe('<span class="glyphicon glyphicon-{0}"></span>'.format(name))


def urls(model,form_class=None,redirect=None,object_list=None,fail_if_empty=True):
    """
    Returns URL patterns for creating, updating and deleting models. Supports lists and formsets as well
    
    model          Model class
    form_class     Form class for use in create, update and formset views (default is None)
    redirect       Redirection URL for create, update and delete views
    object_list    Queryset for list and formset
    fail_if_empty  Raise ImproperlyConfigured exception in formset and list views when object_list is empty
    """
    
    prefix = model.__name__.lower()
    if not redirect: redirect = reverse_lazy(prefix + '_list')
    
    urlpatterns = patterns('',
        # Create a new record
        url('^' + prefix + '/create/',
            CreateView.as_view(model=model,form_class=form_class,success_url=redirect),
            name = prefix + '_create'
        ),
                            
        # Update record 'pk'
        url('^' + prefix + '/update/(?P<pk>\d+)/',
            UpdateView.as_view(model=model,form_class=form_class,success_url=redirect),
            name = prefix + '_update'
        ),
        
        # Delete record 'pk'
        url('^' + prefix + '/delete/(?P<pk>\d+)/',
            DeleteView.as_view(model=model,success_url=redirect),
            name = prefix + '_delete'
        ),

        # List records
        url('^' + prefix + '/list/',
            ListView.as_view(model=model,object_list=object_list,fail_if_empty=fail_if_empty),
            name = prefix + '_list'
        ),
                            
        # Edit records using a formset
        url('^' + prefix + '/formset/',
            FormsetView.as_view(model=model,form_class=form_class,object_list=object_list,fail_if_empty=fail_if_empty),
            name = prefix + '_formset'
        ),
                            
    )
    
    return urlpatterns




def _std_context(self,context,default_title):
    context['template_title'] = self.template_title or default_title
    if self.template_subtitle: context['template_subtitle'] = self.template_subtitle
        
    context['widget'] = self.widget
    
    if self.attributes: context['attributes'] = self.attributes

    context['settings'] = settings.CRUD_SETTINGS
    
    return context
    



class CreateView(vanilla.CreateView):
    """
    Create view for generic model, based on django-vanilla-views
    
    Note: get_form() adds request to the form kwargs
    """
    
    template_name = 'crud/container.html'
    widget = 'crud/widget/form.html'     
    template_title = None
    template_subtitle = None
    attributes = None

    
    def get_context_data(self, **kwargs):
        context = super(CreateView,self).get_context_data(**kwargs)
        context = _std_context(self,context,_('New ' + unicode(self.model._meta.verbose_name)))
        return context
    
    
    def form_valid(self, form):
        out = super(CreateView,self).form_valid(form)
        messages.success(self.request,self.get_success_message())
        return out
    
    def get_success_message(self):
        return _('New {0} saved'.format(self.model._meta.verbose_name.title()))




class UpdateView(vanilla.UpdateView):
    """
    Update view for generic model, based on django-vanilla-views
    
    Note: get_form() adds request to the form kwargs
    """

    template_name = 'crud/container.html'
    widget = 'crud/widget/form.html'     
    template_title = None
    template_subtitle = None
    attributes = None

    
    def get_context_data(self, **kwargs):
        context = super(UpdateView,self).get_context_data(**kwargs)
        context = _std_context(self,context,_('Update ' + unicode(self.model._meta.verbose_name)))        
        return context

    
    def form_valid(self, form):
        out = super(UpdateView,self).form_valid(form)
        messages.success(self.request,self.get_success_message())
        return out
    
    def get_success_message(self):
        return _('{0} saved'.format(self.model._meta.verbose_name.title()))

    
    
        
class DeleteView(vanilla.DeleteView):
    template_name = 'crud/container.html'
    widget = 'crud/widget/delete.html'     
    template_title = None
    template_subtitle = None
    attributes = None


    def get_context_data(self, **kwargs):
        context = super(DeleteView,self).get_context_data(**kwargs)
        context = _std_context(self,context,_('Delete ' + unicode(self.model._meta.verbose_name)))        
        return context




class ListView(vanilla.ListView):
    """
    List model view

    Must define 'object_list' or override get_object_list(self)
    """
    
    template_title = None
    template_subtitle = None
    object_list = None # collection of objects (e.g. queryset or list)
    attributes = None

    template_name = 'crud/container.html'
    widget = 'crud/widget/table.html'
    value_widget = 'crud/widget/value.html'
    
    fail_if_empty = True # Raise ImproperlyConfigured if list is empty, otherwise show empty page
    

    def get_queryset(self):
        "Deprecated, for compatibility with vanilla.ListView. Use get_object_list() instead"
        return self.get_object_list()
        
    def get_object_list(self):
        if not self.object_list and self.fail_if_empty:
            raise ImproperlyConfigured('Define {0}.object_list or override {0}.get_object_list()'.format(self.__class__.__name__))
        
        return self.object_list
      
    def get_context_data(self, **kwargs):
        context = super(ListView,self).get_context_data(**kwargs)
        context = _std_context(self,context,_('List ' + unicode(self.model._meta.verbose_name_plural)))    
        context['value_widget'] = self.value_widget
        
        if 'attributes' not in context:
            prefix = self.model.__name__.lower()
            attr = {}
            attr['links'] = (
                {'label':"Create New",'url':prefix+'_create'},
                {'label':"Edit",'url':prefix+'_formset'}
            )
            
            attr['item_links'] = (
                #(crud.render_glyphicon('eye-open'),prefix+'_detail'),
                {'label':render_glyphicon('pencil'),'url':prefix+'_update','class':'btn btn-sm btn-default'},
                {'label':render_glyphicon('remove'),'url':prefix+'_delete','class':'btn btn-sm btn-danger'},
            )
            
            attr['exclude_fields'] = ['id']

            context['attributes'] = attr
            
        return context

    


class FormsetView(vanilla.CreateView):
    """
    Class view for a generic formset, based on django-vanilla-views

    If parent is set, Expects to be called with a 'pk' that points to the reference model
    """

    parent = None # Define if formset is inline (optional, if None use standard formset)
    object_list = None # A queryset can also be defined directly
    initial = None # if creating new records (with attributes_extra) must define initial or override get_initial()
    
    template_title = None
    template_subtitle = None
    attributes = None
    
    template_name = 'crud/container.html'
    widget = 'crud/widget/formset.html'
    
    fail_if_empty = True # Raise ImproperlyConfigured if list is empty, otherwise show empty page
    
    
    def get_object_list(self):
        if not self.object_list and self.fail_if_empty:
            raise ImproperlyConfigured('Define {0}.object_list or override {0}.get_object_list()'.format(self.__class__.__name__))

        return self.object_list


    def get_form_class(self):
        form_class = super(FormsetView,self).get_form_class()
        extra = self.attributes['extra'] if self.attributes and 'extra' in self.attributes else 0
        formset_class = modelformset_factory(self.model,form=form_class,extra=extra,can_delete=False)  
        return formset_class
    
    
    def get_form(self, data=None, files=None, **kwargs):
        formset_class = self.get_form_class()
        formset = formset_class(data=data,files=files,**kwargs)
        return formset

    
    def get_initial(self):
        if not self.initial and self.attributes and 'extra' in self.attributes:
            raise ImproperlyConfigured("If attributes['extra'] is set must define {0}.initial or override {0}.get_initial()".format(self.__class__.__name__))

        return self.initial
        

    def get_context_data(self,form,**kwargs):
        context = super(FormsetView,self).get_context_data(**kwargs)
        context = _std_context(self,context,_('Edit ' + unicode(self.model._meta.verbose_name_plural)))
        context['formset'] = self.get_form(queryset = self.get_object_list(),initial=self.get_initial())        
        return context
    
    
    def form_valid(self, form):
        out = super(FormsetView,self).form_valid(form)
        messages.success(self.request,self.get_success_message())
        return out
    
    
    def get_success_message(self):
        return _('{0} saved'.format(self.model._meta.verbose_name.title()))


    


