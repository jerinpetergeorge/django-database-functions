from django.db.models.expressions import Func
from django_database_functions.utils import Format
from django.db.models import CharField, IntegerField, DateField

basic_template = '%(function)s(%(expressions)s)'


class CONVERT_TZ(Func):
    function = 'CONVERT_TZ'
    template = "%(function)s(%(expressions)s,'%(from_tz)s', '%(to_tz)s')"

    def __init__(self, *expressions, **extra):
        from_tz = extra.pop('from_tz', None)
        to_tz = extra.pop('to_tz', None)
        extra['output_field'] = CharField()
        assert from_tz is not None, "from_tz must be provided"
        assert to_tz is not None, "to_tz must be provided"
        self.template = self.template % Format({"from_tz": from_tz, "to_tz": to_tz})
        super().__init__(*expressions, **extra)


class DATE(Func):
    function = 'DATE'
    template = basic_template

    def __init__(self, *expressions, **extra):
        if not extra.get('output_field'):
            extra['output_field'] = DateField()
        super().__init__(*expressions, **extra)


class DAYNAME(Func):
    function = 'DAYNAME'

    def __init__(self, *expressions, **extra):
        extra['output_field'] = CharField()
        super().__init__(*expressions, **extra)


class DAYOFMONTH(Func):
    function = 'DAYOFMONTH'

    def __init__(self, *expressions, **extra):
        extra['output_field'] = IntegerField()
        super().__init__(*expressions, **extra)


class EXTRACT(Func):
    function = 'EXTRACT'
    template = '%(function)s(%(unit)s FROM %(expressions)s)'

    def __init__(self, *expressions, **extra):
        unit = extra.pop('unit', 'YEAR')
        if not extra.get('output_field'):
            extra['output_field'] = IntegerField()
        self.template = self.template % Format({"unit": unit})
        super().__init__(*expressions, **extra)


class TIMESTAMPDIFF(Func):
    def __init__(self, *expressions, **extra):
        unit = extra.pop('unit', 'day')
        self.template = self.template % Format({"unit": unit})
        super().__init__(*expressions, **extra)

    function = 'TIMESTAMPDIFF'
    template = "%(function)s(%(unit)s, %(expressions)s)"
