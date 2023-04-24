from django.contrib.auth import get_user_model
from django.db import models

from solotodo.models import Website, Category, Product


class VisitQuerySet(models.QuerySet):
    def filter_by_user_perms(self, user, permission):
        synth_permissions = {
            'view_visit': {
                'category': 'view_category_visits',
                'website': 'view_website_visits'
            }
        }

        assert permission in synth_permissions

        permissions = synth_permissions[permission]

        perm_categories = Category.objects.filter_by_user_perms(
            user, permissions['category'])
        perm_websites = Website.objects.filter_by_user_perms(
            user, permissions['website'])

        qs = self.filter(
            product__instance_model__model__category__in=perm_categories,
            website__in=perm_websites,
        )

        return qs


class Visit(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    website = models.ForeignKey(Website, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    ip = models.GenericIPAddressField()

    objects = VisitQuerySet.as_manager()

    def __str__(self):
        return '{} - {}'.format(self.product, self.timestamp)

    class Meta:
        app_label = 'solotodo'
        ordering = ('-timestamp', )
        permissions = (
            ('view_visits_user_data',
             'Can view the IP and user associated to all visits'),
            ('backend_list_visits', 'Can view list of visits in the backend'),
        )
