from django.conf.urls import url, patterns
from django.contrib import admin
from functools import update_wrapper
from django.shortcuts import redirect
from django.contrib.admin.util import unquote

class ButtonAdmin(admin.ModelAdmin):
    change_buttons=[]
    list_buttons=[]

    change_form_template = 'adminbuttons/change_form_buttons.html'
    change_list_template = 'adminbuttons/change_list_buttons.html'

    def button_view_dispatcher(self, request, url):
        # Dispatch the url to a function call
        if url is not None:
            import re
            res = re.match('(.*/)?(?P<id>\d+)/(?P<command>.*)', url)
            if res:
                if res.group('command') in [b.func_name for b in 
self._get_change_buttons(res.group('id'))]:
                    obj = self.model._default_manager.get(pk=res.group('id'))
                    response = getattr(self, res.group('command'))(request, obj)
                    if response is None:
                        return redirect(request.META['HTTP_REFERER'])
                    return response
            else:
                res = re.match('(.*/)?(?P<command>.*)', url)
                if res:
                    if res.group('command') in [b.func_name for b in 
self._get_list_buttons()]:
                        response = getattr(self, res.group('command'))(request)
                        if response is None:
                            return redirect(request.META['HTTP_REFERER'])
                        return response
        # Delegate to the appropriate method, based on the URL.
        if url is None:
            return self.changelist_view(request)
        elif url == "add":
            return self.add_view(request)
        elif url.endswith('/history'):
            return self.history_view(request, unquote(url[:-8]))
        elif url.endswith('/delete'):
            return self.delete_view(request, unquote(url[:-7]))
        else:
            return self.change_view(request, unquote(url))

    def get_urls(self):
        # Define a wrapper view
        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)
            return update_wrapper(wrapper, view)
        #  Add the custom button url
        urlpatterns = patterns('',
            url(r'^(.+)/$', wrap(self.button_view_dispatcher),)
        )
        return urlpatterns + super(ButtonAdmin, self).get_urls()

    def change_view(self, request, object_id, form_url='', extra_context=None):
        if not extra_context: extra_context = {}
        buttons = self._get_change_buttons(object_id)
        extra_context['buttons'] = self._convert_buttons(buttons)
        if '/' in object_id:
            object_id = object_id[:object_id.find('/')]
        return super(ButtonAdmin, self).change_view(request, object_id, form_url, 
extra_context)

    def changelist_view(self, request, extra_context=None):
        if not extra_context: extra_context = {}
        buttons = self._get_list_buttons()
        extra_context['buttons'] = self._convert_buttons(buttons)
        return super(ButtonAdmin, self).changelist_view(request, extra_context)

    def _get_list_buttons(self):
        entity = getattr(self, 'list_buttons', False)
        buttons = []
        if entity:
            if callable(entity):
                buttons = self.list_buttons()
            else:
                buttons = self.list_buttons
        return buttons

    def _get_change_buttons(self, object_id):
        entity = getattr(self, 'change_buttons', False)
        buttons = []
        if entity:
            if callable(entity):
                buttons = self.change_buttons(object_id)
            else:
                buttons = self.list_buttons        
        return buttons

    def _convert_buttons(self, orig_buttons):
        return [{'func_name': b.func_name, 'short_description': b.short_description} for b 
in orig_buttons]
