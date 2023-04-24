from collections import defaultdict

from django import forms
from django.db import models, IntegrityError
from django.db.models import Q
from sorl.thumbnail.admin.current import AdminImageWidget


class MetaModel(models.Model):
    name = models.CharField(max_length=100, unique=True)
    unicode_template = models.CharField(max_length=255, null=True, blank=True)
    ordering_field = models.CharField(max_length=50, null=True, blank=True)

    default_class = {'class': 'form-control'}

    NAME_INPUT_TYPES_DICT = {
        'BooleanField': ('checkbox', forms.CheckboxInput()),
        'CharField': ('text', type('CharInput',
                                   (forms.TextInput, ),
                                   {'input_type': 'text'})(default_class)),
        'DateField': ('date', type('DateInput', (forms.DateInput, ),
                                   {'input_type': 'date'})(format='%Y-%m-%d')),
        'DateTimeField': ('datetime-local',
                          type('DateTimeInput',
                               (forms.DateTimeInput, ),
                               {'input_type': 'datetime-local'})(
                              attrs={
                                  'format': '%Y-%m-%dT%H:%M',
                                  'class': 'form-control'}
                          )),
        'DecimalField': ('number', type('DecimalInput',
                                        (forms.TextInput, ),
                                        {'input_type': 'number'})(
            attrs={'step': '0.001', 'class': 'form-control'}
        )),
        'FileField': ('file', AdminImageWidget()),
        'IntegerField': ('number', type('IntegerInput',
                                        (forms.TextInput, ),
                                        {'input_type': 'number'})(
            default_class
        )),
    }

    PRIMITIVE_MODELS_DICT = None
    METAMODEL_MODELS_DICT = None
    METAMODEL_MODELS_FIELDS_DICT = None

    def __str__(self):
        return self.name

    def is_primitive(self):
        return self.name in MetaModel.NAME_INPUT_TYPES_DICT

    def html_input_type(self):
        return MetaModel.NAME_INPUT_TYPES_DICT[self.name][0]

    def get_form(self):
        form_klass = type('MetaModelForm', (forms.Form, ), {})

        for field in self.fields.filter(hidden=False):
            form_klass.base_fields[field.name] = field.get_form_field()

        return form_klass

    def delete(self, *args, **kwargs):
        from metamodel.models import InstanceField

        if self.is_primitive():
            raise IntegrityError('Cannot delete primitive fields')

        primitive_instance_fields = InstanceField.objects.filter(
            field__parent=self,
            field__model__in=MetaModel.get_primitive()
        )

        for field in primitive_instance_fields:
            field.value.delete()

        super(MetaModel, self).delete(*args, **kwargs)

    @classmethod
    def convert_model_field(cls, model_field):
        model_field_class = model_field.__class__

        if model_field_class.__name__ in cls.NAME_INPUT_TYPES_DICT.keys():
            return model_field_class

        if model_field_class.__name__ == 'ImageField':
            return models.FileField

        if model_field.__class__.__name__ == 'URLField':
            return models.CharField

        if model_field.__class__.__name__ == 'TextField':
            return models.CharField

        if model_field.__class__.__name__ == 'CommaSeparatedIntegerField':
            return models.CharField

        if model_field.__class__.__name__ == 'AutoField':
            return models.IntegerField

        if model_field_class.__name__ in ['ForeignKey', 'ManyToManyField']:
            return model_field.related.parent_model

        raise Exception('No compatible model found: {0} - {1}'.format(
            model_field_class, model_field.name))

    @classmethod
    def get_non_primitive(cls):
        return cls.objects.filter(
            ~Q(name__in=cls.NAME_INPUT_TYPES_DICT.keys()))

    @classmethod
    def get_primitive(cls):
        return cls.objects.filter(name__in=cls.NAME_INPUT_TYPES_DICT.keys())

    @classmethod
    def get_primitive_models_dict(cls):
        if cls.PRIMITIVE_MODELS_DICT is None:
            primitive_models = cls.get_primitive()
            result = {m.id: m for m in primitive_models}
            cls.PRIMITIVE_MODELS_DICT = result

        return cls.PRIMITIVE_MODELS_DICT

    @classmethod
    def get_model_by_id(cls, model_id):
        def get_models_dict(refresh_cache=False):
            if not cls.METAMODEL_MODELS_DICT or refresh_cache:
                result = {m.id: m for m in cls.objects.all()}
                cls.METAMODEL_MODELS_DICT = result

            return cls.METAMODEL_MODELS_DICT

        models_dict = get_models_dict()
        meta_field = models_dict.get(model_id, None)
        if meta_field:
            return meta_field
        else:
            models_dict = get_models_dict(refresh_cache=True)
            return models_dict[model_id]

    @classmethod
    def get_metafields_by_model_id(cls, model_id):
        def get_model_fields_dict(refresh_cache=False):
            from metamodel.models import MetaField

            if not cls.METAMODEL_MODELS_FIELDS_DICT or refresh_cache:
                fields = MetaField.objects.order_by('parent').select_related()

                result = {}

                for field in fields:
                    if field.parent_id not in result:
                        result[field.parent_id] = []
                    result[field.parent_id].append(field)
                cls.METAMODEL_MODELS_FIELDS_DICT = result

            return cls.METAMODEL_MODELS_FIELDS_DICT

        models_dict = get_model_fields_dict()
        meta_fields = models_dict.get(model_id, None)
        if meta_fields:
            return meta_fields
        else:
            models_dict = get_model_fields_dict(refresh_cache=True)
            return models_dict[model_id]

    @staticmethod
    def generate_metamodel_structure():
        from . import MetaModel, InstanceModel

        from metamodel.serializers import MetaModelPlainSerializer
        from metamodel.serializers import InstanceModelPlainSerializer

        from metamodel.models import MetaField
        from metamodel.models import InstanceField
        from metamodel.serializers import MetaFieldPlainSerializer
        from metamodel.serializers import InstanceFieldPlainSerializer
        metamodel_data = [
            {
                'klass': MetaModel,
                'fields_klass': MetaField,
                'prefix': 'MM',
                'serializer': MetaModelPlainSerializer,
                'fields_serializer': MetaFieldPlainSerializer

            },
            {
                'klass': InstanceModel,
                'fields_klass': InstanceField,
                'prefix': 'IM',
                'serializer': InstanceModelPlainSerializer,
                'fields_serializer': InstanceFieldPlainSerializer
            }
        ]

        d = {}

        for metamodel_entry in metamodel_data:
            print(metamodel_entry['klass'])
            print('Loading fields')
            fields_objects = metamodel_entry['fields_klass'].objects.all()
            print('Creating field serializer')
            fields_data = metamodel_entry['fields_serializer'](fields_objects, many=True).data
            print('Creating field dict')
            fields_per_parent = defaultdict(lambda: [])
            for field_data in fields_data:
                fields_per_parent[field_data['parent_id']].append(field_data)

            print('Loading objects')
            mm_objects = metamodel_entry['klass'].objects.all()
            print('Creating objects serializer')
            serializer = metamodel_entry['serializer']
            serialized_objects = serializer(mm_objects, many=True).data

            print('Assembling final dict')
            for serialized_object in serialized_objects:
                serialized_object['fields'] = fields_per_parent.get(serialized_object['id'], [])
                d_key = '{}_{}'.format(metamodel_entry['prefix'], serialized_object['id'])
                d[d_key] = serialized_object

        return d


    class Meta:
        app_label = 'metamodel'
        ordering = ('name', )
