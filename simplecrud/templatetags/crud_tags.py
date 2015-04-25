from django import template
from django.db import models
from django.utils.safestring import mark_safe

from simplecrud.format import format_value,auto_precision


# TODO: field_titles_and_values misses m2m fields because model._meta._fields ignores those

register = template.Library()


@register.filter(name='fields_from_model')
def fields_from_model(model):
    return model._meta.fields
    #return [field for field in model._meta.fields]



@register.filter(name='field_titles_and_values')
def field_titles_and_values(model,options=None):
    show_all = False
    
    if options:
        if 'include_fields' in options:
            includes = options['include_fields']
            field_list = [f for f in model._meta.fields if f.name in includes]
        else:
            field_list = model._meta.fields
            
        if 'exclude_fields' in options:
            excludes = options['exclude_fields']
            field_list = [f for f in field_list if f.name not in excludes]

        show_all = options['show_all'] if 'show_all' in options else False        
        bool_as_icon = options['bool_as_icon'] if 'bool_as_icon' in options else True
        
    else:
        field_list = model._meta.fields
        
    out = [
        (field.verbose_name,_field_value(model,field,bool_as_icon)) 
        for field in field_list
        if show_all or _field_value(model,field,bool_as_icon)
    ]
    
    return out




@register.filter(name='field_value')
def field_value(model,field):
    return getattr(model,field)




@register.filter(name='auto_format_value')
def auto_format_value(value):
    prec = auto_precision(value)
    return format_value(value,"f" + str(prec))

 
            

@register.filter(name='format_value')
def format_value(value,number_format):
    return format_value(value,number_format)




@register.filter(name='is_sequence')
def is_sequence(value):
    return isinstance(value,(tuple,list))


            

def _field_value(model,field,bool_as_icon):
    v = getattr(model,field.name)
    
    if isinstance(field,models.BooleanField) and bool_as_icon:
        if v: return mark_safe('<span class="glyphicon glyphicon-ok"></span>') #"ICON:OK"
        else: return mark_safe('<span class="glyphicon glyphicon-remove"></span>') #"ICON:REMOVE"

    if hasattr(field,'choices') and field.choices:
        return dict(field.choices).get(v,'')

    return v



