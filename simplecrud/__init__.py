from __future__ import unicode_literals

import vanilla

from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.forms.models import modelformset_factory
from django.shortcuts import redirect
from django.utils.safestring import mark_safe
from django.contrib import messages
from django.http import Http404
from django.conf import settings


# TODO: Edit, add and delete buttons are visible and active even if user has no modification/deletion rights to a model. Make these buttons sensitive to the setting
# TODO: Raise error is settings.CRUD_SETTINGS doesn't exist


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


def _std_context(self,context,default_title=None):
    if self.template_title is None:
        context['template_title'] = default_title
    else:
        context['template_title'] = self.template_title

    if self.template_subtitle: context['template_subtitle'] = self.template_subtitle
        
    if self.widget is None: raise ImproperlyConfigured("Widget not set in type {}".format(type(self)))
    context['widget'] = self.widget
    
    if self.attributes: context['attributes'] = self.attributes

    if hasattr(settings,'SIMPLECRUD'):
        context['simplecrud'] = settings.SIMPLECRUD
    else:
        context['simplecrud'] = {}

    return context
    


class PermissionMixin(object):
    def check_permission(self,request,*args,**kwargs):
        return True
    
    def dispatch(self,request,*args,**kwargs):
        if not self.check_permission(request,*args,**kwargs): raise Http404
        return super(PermissionMixin,self).dispatch(request,*args,**kwargs)




RedirectView = vanilla.RedirectView # vanilla.RedirectView here only for completness




class TemplateView(PermissionMixin,vanilla.TemplateView):
    """
    Implementation of the standard TemplateView with support for the simplecrud header and footer
    """
    
    template_name = 'simplecrud/container.html'
    widget = None     
    template_title = None
    template_subtitle = None
    attributes = None

    def get_context_data(self, **kwargs):
        context = super(TemplateView,self).get_context_data(**kwargs)
        context = _std_context(self,context)
        return context




class CreateView(PermissionMixin,vanilla.CreateView):
    """
    Create view for generic model, based on django-vanilla-views
    
    Note: get_form() adds request to the form kwargs
    """
    
    template_name = 'simplecrud/container.html'
    widget = 'simplecrud/widget/form.html'     
    template_title = None
    template_subtitle = None
    attributes = None

    
    def get_context_data(self, **kwargs):
        context = super(CreateView,self).get_context_data(**kwargs)
        model_name = unicode(self.model._meta.verbose_name) if self.model else 'Object'
        context = _std_context(self,context,_('New ' + model_name))
        return context
    
    
    def form_valid(self, form):
        out = super(CreateView,self).form_valid(form)
        messages.success(self.request,self.get_success_message())
        return out
    
    def get_success_message(self):
        return _('New {0} saved'.format(self.model._meta.verbose_name.title()))




class UpdateView(PermissionMixin,vanilla.UpdateView):
    """
    Update view for generic model, based on django-vanilla-views
    
    Note: get_form() adds request to the form kwargs
    """

    template_name = 'simplecrud/container.html'
    widget = 'simplecrud/widget/form.html'     
    template_title = None
    template_subtitle = None
    attributes = None

    
    def get_context_data(self, **kwargs):
        context = super(UpdateView,self).get_context_data(**kwargs)
        model_name = unicode(self.model._meta.verbose_name) if self.model else 'Object'
        context = _std_context(self,context,_('Update ' + model_name))        
        return context

    
    def form_valid(self, form):
        out = super(UpdateView,self).form_valid(form)
        messages.success(self.request,self.get_success_message())
        return out
    
    def get_success_message(self):
        return _('{0} saved'.format(self.model._meta.verbose_name.title()))

    
    
        
class DeleteView(PermissionMixin,vanilla.DeleteView):
    template_name = 'simplecrud/container.html'
    widget = 'simplecrud/widget/delete.html'     
    template_title = None
    template_subtitle = None
    attributes = None


    def get_context_data(self, **kwargs):
        context = super(DeleteView,self).get_context_data(**kwargs)
        model_name = unicode(self.model._meta.verbose_name) if self.model else 'Object'
        context = _std_context(self,context,_('Delete ' + model_name))        
        return context




class ListView(PermissionMixin,vanilla.ListView):
    """
    List model view

    Must define 'object_list' or override get_object_list(self)
    """
    
    template_title = None
    template_subtitle = None
    object_list = None # collection of objects (e.g. queryset or list)
    attributes = None

    template_name = 'simplecrud/container.html'
    widget = 'simplecrud/widget/table.html'
    value_widget = 'simplecrud/widget/value.html'
    
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
        
        model_name = unicode(self.model._meta.verbose_name_plural) if self.model else 'Objects'
        context = _std_context(self,context,_('List ' + model_name))    
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

    


class FormsetView(PermissionMixin,vanilla.CreateView):
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
    
    template_name = 'simplecrud/container.html'
    widget = 'simplecrud/widget/formset.html'
    
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


    


