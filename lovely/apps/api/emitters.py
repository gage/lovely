from __future__ import generators

import decimal, re, inspect

try:
    # yaml isn't standard with python.  It shouldn't be required if it
    # isn't used.
    import yaml
except ImportError:
    yaml = None

# Fallback since `any` isn't in Python <2.5
try:
    any
except NameError:
    def any(iterable):
        for element in iterable:
            if element:
                return True
        return False

from django.db.models.query import QuerySet
from django.db.models import Model, permalink
from django.utils import simplejson
from django.utils.xmlutils import SimplerXMLGenerator
from django.utils.encoding import smart_unicode
from django.core.serializers.json import DateTimeAwareJSONEncoder
from django.http import HttpResponse
from django.core import serializers
#================================================================Modify start===============================================#
from django.contrib.auth.models import User
from datetime import date
import time
#================================================================Modify end===============================================#

#Field rename through field_dict
# origin_field = ['main_pic', 'user_id', 'image500x500', 'image185x185', 'image50x50' , 'main_profile_pic', 'cover', 'district']
# target_field = ['photo'   , 'id'     , 'image_large' , 'image_medium', 'image_small', 'photo'           , 'photo', 'region']
# field_dict = dict(zip(origin_field,target_field))
field_dict = {}
#Modify

ELIMINATE_INDENT = False

try:
    import cStringIO as StringIO
except ImportError:
    import StringIO

try:
    import cPickle as pickle
except ImportError:
    import pickle

from piston.emitters import Emitter
from piston.utils import HttpStatusCode, Mimer

class GuluEmitter(Emitter):
    def __init__(self, payload, typemapper, handler, fields=(), anonymous=True, request=None):
        self.typemapper = typemapper
        self.data = payload
        self.handler = handler
        self.fields = fields
        self.anonymous = anonymous
        self.request = request
        
        if isinstance(self.data, Exception):
            raise
        
    def construct(self):
        """
        Recursively serialize a lot of types, and
        in cases where it doesn't recognize the type,
        it will fall back to Django's `smart_unicode`.
        
        Returns `dict`.
        """
        def _any(thing, fields=()):
            """
            Dispatch, all types are routed through here.
            """
            ret = None
            
            if isinstance(thing, QuerySet):
                ret = _qs(thing, fields=fields)
            elif isinstance(thing, (tuple, list)):
                ret = _list(thing)
            elif isinstance(thing, dict):
                ret = _dict(thing)
            elif isinstance(thing, decimal.Decimal):
                ret = str(thing)
            elif isinstance(thing, Model):
                #==Modify start==#
                if isinstance(thing, User):
                    ret = _model(thing.get_profile())
                else:                
                    ret = _model(thing, fields=fields)
                #==Modify end===#                
            elif isinstance(thing, HttpResponse):
                raise HttpStatusCode(thing)
            elif inspect.isfunction(thing):
                if not inspect.getargspec(thing)[0]:
                    ret = _any(thing())
            elif hasattr(thing, '__emittable__'):
                f = thing.__emittable__
                if inspect.ismethod(f) and len(inspect.getargspec(f)[0]) == 1:
                    ret = _any(f())            
            #==Modify start==#
            elif isinstance(thing, date): 
                ret = str(time.mktime(thing.timetuple())) #Convert to unix time
            #==Modify end==#
            else:                                
                ret = smart_unicode(thing, strings_only=True)
                
            return ret

        def _fk(data, field):
            """
            Foreign keys.
            """
            return _any(getattr(data, field.name))
        
        def _related(data, fields=()):
            """
            Foreign keys.
            """
            return [ _model(m, fields) for m in data.iterator() ]
        
        def _m2m(data, field, fields=()):
            """
            Many to many (re-route to `_model`.)
            """
            return [ _model(m, fields) for m in getattr(data, field.name).iterator() ]
        #==Modify start==#
        def _m2m_costum(data, field, fields=()):
            """
            Costum Many to many (re-route to `_model`.)
            """
            return [ _any(m, fields) for m in getattr(data, field).get_query_set() ]        
        #==Modify end==#
        
        def _model(data, fields=()):
            """
            Models. Will respect the `fields` and/or
            `exclude` on the handler (see `typemapper`.)
            """
            ret = { }
            handler = self.in_typemapper(type(data), self.anonymous)
            get_absolute_uri = False
            
            if handler or fields:
                v = lambda f: getattr(data, f.attname)

                if not fields:
                    """
                    Fields was not specified, try to find teh correct
                    version in the typemapper we were sent.
                    """
                    mapped = self.in_typemapper(type(data), self.anonymous)
                    get_fields = set(mapped.fields)
                    exclude_fields = set(mapped.exclude).difference(get_fields)

                    if 'absolute_uri' in get_fields:
                        get_absolute_uri = True
                
                    if not get_fields:
                        get_fields = set([ f.attname.replace("_id", "", 1)
                            for f in data._meta.fields ])
                
                    # sets can be negated.
                    for exclude in exclude_fields:
                        if isinstance(exclude, basestring):
                            get_fields.discard(exclude)
                            
                        elif isinstance(exclude, re._pattern_type):
                            for field in get_fields.copy():
                                if exclude.match(field):
                                    get_fields.discard(field)
                                    
                else:
                    get_fields = set(fields)

                met_fields = self.method_fields(handler, get_fields)

                for f in data._meta.local_fields:
                    if f.serialize and not any([ p in met_fields for p in [ f.attname, f.name ]]):                        
                        if not f.rel:
                            """Modify: handle normal attributes"""
                            if f.attname in get_fields:                                                                
                                if f.attname in origin_field: #origin_field
                                    ret[field_dict[f.attname]] = _any(v(f))                                    
                                else:
                                    ret[f.attname] = _any(v(f))                                                                                      
                                get_fields.remove(f.attname)
                                
                        else:
                            """Modify: handle the object, net structure"""
                            if f.attname[:-3] in get_fields:                                
                                if f.attname[:-3] in origin_field: #origin_field
                                    ret[ field_dict[f.attname[:-3]] ] = _fk(data, f)
                                else:
                                    ret[f.name] = _fk(data, f)                                    
                                get_fields.remove(f.name)
                                
                
                """Modify: handle the queryset like Manager""" 
                for mf in data._meta.many_to_many:
                    if mf.serialize and mf.attname not in met_fields:
                        if mf.attname in get_fields:
                            ret[mf.name] = _m2m(data, mf)
                            get_fields.remove(mf.name)
                
                # try to get the remainder of fields
                
                for maybe_field in get_fields:
                    if isinstance(maybe_field, (list, tuple)):
                        model, fields = maybe_field
                        inst = getattr(data, model, None)

                        if inst:
                            if hasattr(inst, 'all'):
                                ret[model] = _related(inst, fields)
                            elif callable(inst):
                                if len(inspect.getargspec(inst)[0]) == 1:
                                    ret[model] = _any(inst(), fields)                                                                    
                            else:
                                """Modify: handle the image fields"""
                                if model in origin_field: #origin_field
                                    ret[field_dict[model]] = _model(inst, fields)
                                else:
                                    ret[model] = _model(inst, fields)                                    
                                #Modify
                                
                                
                    elif maybe_field in met_fields:
                        # Overriding normal field which has a "resource method"
                        # so you can alter the contents of certain fields without
                        # using different names.
                        ret[maybe_field] = _any(met_fields[maybe_field](data))
                    else:
                        maybe = getattr(data, maybe_field, None)
                        if maybe:
                            if callable(maybe):
                                if len(inspect.getargspec(maybe)[0]) == 2 and 'request' in inspect.getargspec(maybe)[0]:
                                    ret[maybe_field] = _any(maybe(self.request))
                                elif len(inspect.getargspec(maybe)[0]) == 1:
                                    ret[maybe_field] = _any(maybe())
                            else:
                                if hasattr(maybe, '_get_pk_list'): #M2M                  
                                    ret[maybe_field] = _m2m_costum(data, maybe_field)
                                elif maybe_field in origin_field: #origin_field
                                    ret[field_dict[maybe_field]] = _any(maybe)
                                else:
                                    ret[maybe_field] = _any(maybe)
                                    # For the . . api
                                    if maybe_field == 'place':
                                        ret['restaurant'] = ret['place']                    
                                    
                        else:
                            handler_f = getattr(handler or self.handler, maybe_field, None)

                            if handler_f:
                                ret[maybe_field] = _any(handler_f(data))

            else:
                for f in data._meta.fields:                    
                    ret[f.attname] = _any(getattr(data, f.attname))
                
                fields = dir(data.__class__) + ret.keys()
                add_ons = [k for k in dir(data) if k not in fields]
                
                for k in add_ons:
                    ret[k] = _any(getattr(data, k))
            
            # resouce uri
            if self.in_typemapper(type(data), self.anonymous):
                handler = self.in_typemapper(type(data), self.anonymous)
                if hasattr(handler, 'resource_uri'):
                    url_id, fields = handler.resource_uri()
                    ret['resource_uri'] = permalink( lambda: (url_id, 
                        (getattr(data, f) for f in fields) ) )()
            
            if hasattr(data, 'get_api_url') and 'resource_uri' not in ret:
                try: ret['resource_uri'] = data.get_api_url()
                except: pass
            
            # absolute uri
            if hasattr(data, 'get_absolute_url') and get_absolute_uri:
                try: ret['absolute_uri'] = data.get_absolute_url()
                except: pass
                
            return ret
        
        def _qs(data, fields=()):
            """
            Querysets.
            """
            return [ _any(v, fields) for v in data ]
                
        def _list(data):
            """
            Lists.
            """
            return [ _any(v) for v in data ]
            
        def _dict(data):
            """
            Dictionaries.
            """
            return dict([ (k, _any(v)) for k, v in data.iteritems() ])
            
        # Kickstart the seralizin'.
        return _any(self.data, self.fields)

    #==Modify start-- Do deferred model deferred process ==#
    def in_typemapper(self, model, anonymous):
        if 'Deferred' in model.__name__:
            model = model.__mro__[1]
        
        for klass, (km, is_anon) in self.typemapper.iteritems():
            if model is km and is_anon is anonymous:
                return klass
    #==Modify end==#
    
    def render(self, request):
        cb = request.GET.get('callback')
        if ELIMINATE_INDENT:
            seria = simplejson.dumps(self.construct(), cls=DateTimeAwareJSONEncoder, ensure_ascii=False)
        else:
            seria = simplejson.dumps(self.construct(), cls=DateTimeAwareJSONEncoder, ensure_ascii=False, indent=3)
        # Callback
        if cb:
            return '%s(%s)' % (cb, seria)

        return seria
    
    def render_to_obj(self):
        return self.construct()
        
    def stream_render(self, request, stream=True):
        """
        Tells our patched middleware not to look
        at the contents, and returns a generator
        rather than the buffered string. Should be
        more memory friendly for large datasets.
        """
        yield self.render(request)
