# -*- coding: utf-8 -*-

from django.core.serializers.json import DjangoJSONEncoder


class Options:

    def __init__(self, **options):
        self.defaults = {}
        self.options = options

    def to_dict(self, include_not_changed=False):
        def _merge(rhs, lhs):
            data = {}
            for rhs_key, rhs_value in rhs.items():
                if rhs_key in lhs:
                    lhs_value = lhs.get(rhs_key)
                    if isinstance(rhs_value, dict) and isinstance(lhs_value, dict):
                        lhs = _merge(rhs_value, lhs_value)
                    else:
                        lhs = rhs
                else:
                    lhs = rhs
                if include_not_changed or rhs != lhs:
                    data[rhs_key] = lhs
            return data

        return _merge(self.defaults, self.options)


class JsonUnquote:
    def __init__(self, data):
        self.data = data

    def __eq__(self, other):
        if isinstance(other, JsonUnquote):
            other = other.data
        elif not isinstance(other, str):
            other = str(other)
        return self.data == other


class OptionsEncoder(DjangoJSONEncoder):

    # def default(self, o):
    #     if isinstance(o, JsonUnquote):
    #         if o.data:
    #             return 'eval("%s")' % o.data
    #     ret = super().default(o)
    #     return ret
    #
    # def encode(self, o):
    #     if isinstance(o, JsonUnquote):
    #         return o.data
    #     return super().encode(o)

    pass
