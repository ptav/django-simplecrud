from django import template
from django.db import models
from crud.format import format_value,auto_precision


register = template.Library()


@register.filter(name='fields_from_model')
def fields_from_model(model):
    return model._meta.fields
    #return [field for field in model._meta.fields]



@register.filter(name='field_titles_and_values')
def field_titles_and_values(model,options=None):
    if options:
        if 'include_fields' in options:
            includes = options['include_fields']
            field_list = [f for f in model._meta.fields if f.name in includes]
        else:
            field_list = model._meta.fields
            
        if 'exclude_fields' in options:
            excludes = options['exclude_fields']
            field_list = [f for f in field_list if f.name not in excludes]

    else:
        field_list = model._meta.fields
        
    out = [(field.verbose_name,_field_value(model,field)) for field in field_list]

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


            

def _field_value(model,field):
    v = getattr(model,field.name)
    
    if isinstance(field,models.BooleanField):
        if v: return "ICON:OK"
        else: return "ICON:REMOVE"

    if hasattr(field,'choices') and field.choices:
        return dict(field.choices).get(v,'')

    return v



