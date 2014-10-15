django-admin-buttons
====================

### Features

 - Add buttons to the django admin change list and edit view.

### Example 1: Change form

![ScreenShot](https://raw.githubusercontent.com/eskildsf/django-admin-buttons/master/screenshots/example.png)

Below is the sample code used to generate the image above. It only shows the
"Export responses" buttons if the survey actually has responses. This is achieved by
making the list of buttons callable (a function returning at list).
	from adminbuttons.django_admin_buttons import ButtonAdmin
	# exportResponses view redirects to the export view.
    def exportResponses(self, request, obj):
        return redirect(reverse('questionnaire:export', args=[obj.id]))
    exportResponses.short_description = 'Export responses'
    # viewSurvey view redirects to the Survey on the website.
    def viewSurvey(self, request, obj):
        return redirect(reverse('questionnaire:survey', args=[obj.id]))
    class SurveyAdmin(ButtonAdmin)
    def change_buttons(self, object_id):
        survey = Survey.objects.get(id=object_id)
        buttons = [self.viewSurvey]
        if survey.hasResponse():
            buttons.append(self.exportResponses)
        return buttons
        
This code shows how to show the "View Survey" button only.
	from adminbuttons.django_admin_buttons import ButtonAdmin
    # viewSurvey view redirects to the Survey on the website.
    def viewSurvey(self, request, obj):
        return redirect(reverse('questionnaire:survey', args=[obj.id]))
    class SurveyAdmin(ButtonAdmin)
    change_buttons = [se.fviewSurvey]

### Example 2: Change list
This example shows how to add a "Clear All" button to a change list in the Django admin.
    from adminbuttons.django_admin_buttons import ButtonAdmin
    class DeviceLogAdmin(ButtonAdmin):
        def clearLogs(self, request):
            # Deletes all log entries
            result = DeviceLog.objects.all()
            action = delete_selected(self, request, result)
            if action is None:
                return redirect(reverse('admin:slideshow_devicelog_changelist'))
            else:
                return action
        clearLogs.short_description = 'Clear logs'
        list_buttons = [clearLogs]
Notice that a specific object is not passed along to the buttons' view.

You could make this example more complex by having the "Clear logs" button only show
up when there are records to delete.

### Authors
 - [Eskild Schroll-Fleischer]

## Installation

1. `pip install git+https://github.com/eskildsf/django-admin-buttons.git`
2. Edit settings.py
3. Add 'adminbuttons' to INSTALLED_APPS

Example:

    INSTALLED_APPS = (
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.sites',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'django.contrib.flatpages',  
        'adminbuttons',
    )


### Help

Create an issue on Github.