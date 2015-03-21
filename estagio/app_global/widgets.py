import django.contrib.admin.widgets
from django.utils.safestring import mark_safe


class NoAddingRelatedFieldWidgetWrapper(django.contrib.admin.widgets.RelatedFieldWidgetWrapper):

    def render(self, name, value, *args, **kwargs):
        from django.contrib.admin.views.main import TO_FIELD_VAR
        rel_to = self.rel.to
        info = (rel_to._meta.app_label, rel_to._meta.model_name)
        self.widget.choices = self.choices
        output = [self.widget.render(name, value, *args, **kwargs)]
        '''
        if self.can_add_related:
            related_url = reverse('admin:%s_%s_add' % info, current_app=self.admin_site.name)
            url_params = '?%s=%s' % (TO_FIELD_VAR, self.rel.get_related_field().name)
            # TODO: "add_id_" is hard-coded here. This should instead use the
            # correct API to determine the ID dynamically.
            output.append('<a href="%s%s" class="add-another" id="add_id_%s" onclick="return showAddAnotherPopup(this);"> '
                          % (related_url, url_params, name))
            output.append('<img src="%s" width="10" height="10" alt="%s"/></a>'
                          % (static('admin/img/icon_addlink.gif'), _('Add Another')))
        '''
        return mark_safe(''.join(output))

# Monkeypatch
django.contrib.admin.widgets.RelatedFieldWidgetWrapper = NoAddingRelatedFieldWidgetWrapper