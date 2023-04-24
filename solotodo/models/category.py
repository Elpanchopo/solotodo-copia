from django.contrib.auth.models import Group
from django.core.cache import cache
from django.db import models
from guardian.shortcuts import get_objects_for_user, get_objects_for_group

from metamodel.models import MetaModel
from solotodo.models.category_tier import CategoryTier


class CategoryQuerySet(models.QuerySet):
    def filter_by_user_perms(self, user, permission, reload_cache=False):
        from solotodo_core import settings

        if user.is_superuser:
            return self

        user_group_names = [x['name'] for x in user.groups.values('name')]

        if permission == 'view_category' and (
                user.is_anonymous or user_group_names ==
                [settings.DEFAULT_GROUP_NAME]):
            return self.filter_viewable_by_default_group(
                reload_cache=reload_cache)

        return get_objects_for_user(user, permission, self)

    def filter_viewable_by_default_group(self, reload_cache=False):
        from solotodo_core import settings

        category_ids = cache.get('default_group_category_ids')
        if not category_ids or reload_cache:
            group = Group.objects.get(name=settings.DEFAULT_GROUP_NAME)
            categories = get_objects_for_group(group, 'view_category',
                                               Category)
            category_ids = [x.id for x in categories]
            cache.set('default_group_category_ids', category_ids)

        return self.filter(pk__in=category_ids)


class Category(models.Model):
    name = models.CharField(max_length=255, db_index=True, unique=True)
    meta_model = models.OneToOneField(MetaModel, on_delete=models.CASCADE,
                                      blank=True, null=True)
    tier = models.ForeignKey(CategoryTier, on_delete=models.CASCADE,
                             blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)
    storescraper_name = models.CharField(
        max_length=255, db_index=True, blank=True, null=True)
    budget_ordering = models.IntegerField(null=True, blank=True)
    suggested_alternatives_ordering = models.CharField(
        max_length=255, blank=True, null=True)
    suggested_alternatives_filter = models.CharField(
        max_length=255, blank=True, null=True)
    similar_products_fields = models.CharField(
        max_length=255, null=True, blank=True)
    search_bucket_key_fields = models.CharField(
        max_length=255, null=True, blank=True)
    detail_bucket_key_fields = models.CharField(
        max_length=255, null=True, blank=True)
    short_description_template = models.TextField(
        blank=True, null=True)
    browse_result_template = models.TextField(
        blank=True, null=True)
    detail_template = models.TextField(
        blank=True, null=True)

    objects = CategoryQuerySet.as_manager()

    def __str__(self):
        return self.name

    def specs_form(self):
        from solotodo.forms.category_specs_form import CategorySpecsForm

        form_class = type(
            'ES{}SpecsForm'.format(self.meta_model.name),
            (CategorySpecsForm,),
            {
                'category': self,
                'category_specs_filters': [],
                'ordering_value_to_es_field_dict': {}
            })

        for category_specs_filter in self.categoryspecsfilter_set.\
                select_related('meta_model'):
            form_class.add_filter(category_specs_filter)

        for category_specs_order in self.categoryspecsorder_set.all():
            form_class.add_order(category_specs_order)

        return form_class

    class Meta:
        app_label = 'solotodo'
        ordering = ['name']
        permissions = (
            ['is_category_staff', 'Is staff of the category'],
            ['view_category_leads',
             'View the leads associated to this category'],
            ['view_category_visits',
             'View the visits associated to this category'],
            ['view_category_reports',
             'Download the reports associated to this category'],
            ['view_category_share_of_shelves',
             'View share of shelves of the category'],
            ['create_category_product_list',
             'Can create a product list in this category'],
            ['create_category_brand_comparison',
             'Can create a brand comparison for this category'],
            ['backend_list_categories', 'View category list in backend'],
            ['view_category_entity_positions',
             'Can view category entity positions'],
            ['create_category_keyword_search',
             'Can create keyword searches in this category']
        )
