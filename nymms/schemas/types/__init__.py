import logging
import collections
import json

logger = logging.getLogger(__name__)

from schematics.types import BaseType
from schematics.exceptions import ValidationError

import arrow


class TimestampType(BaseType):
    def to_native(self, value, context=None):
        if isinstance(value, arrow.arrow.Arrow):
            return value
        return arrow.get(value)

    def to_primitive(self, value, context=None):
        return value.timestamp


class JSONType(BaseType):
    def to_native(self, value, context=None):
        if isinstance(value, basestring):
            return json.loads(value)
        return value

    def to_primitive(self, value, context=None):
        return json.dumps(value)


StateObject = collections.namedtuple('StateObject', ['name', 'code'])
STATE_OK = StateObject('ok', 0)
STATE_WARNING = STATE_WARN = StateObject('warning', 1)
STATE_CRITICAL = STATE_CRIT = StateObject('critical', 2)
STATE_UNKNOWN = StateObject('unknown', 3)
STATES = collections.OrderedDict([
    ('ok', STATE_OK),
    ('warning', STATE_WARNING),
    ('critical', STATE_CRITICAL),
    ('unknown', STATE_UNKNOWN)])


class StateType(BaseType):
    def __init__(self, *args, **kwargs):
        super(StateType, self).__init__(*args, choices=STATES.values(),
                                        **kwargs)

    def to_native(self, value, context=None):
        if isinstance(value, StateObject):
            return value
        try:
            int_value = int(value)
            try:
                return STATES.values()[int_value]
            except IndexError:
                return STATE_UNKNOWN
        except ValueError:
            try:
                return STATES[value.lower()]
            except KeyError:
                raise ValidationError(self.messages['choices'].format(
                    unicode(self.choices)))

    def to_primitive(self, value, context=None):
        return value.code


StateTypeObject = collections.namedtuple('StateTypeObject', ['name', 'code'])
STATE_TYPE_SOFT = StateTypeObject('soft', 0)
STATE_TYPE_HARD = StateTypeObject('hard', 1)
STATE_TYPES = collections.OrderedDict([
    ('soft', STATE_TYPE_SOFT),
    ('hard', STATE_TYPE_HARD)])


class StateTypeType(BaseType):
    def __init__(self, *args, **kwargs):
        super(StateTypeType, self).__init__(*args,
                                            choices=STATE_TYPES.values(),
                                            **kwargs)

    def to_native(self, value, context=None):
        if isinstance(value, StateTypeObject):
            return value
        try:
            return STATE_TYPES.values()[int(value)]
        except ValueError:
            try:
                return STATE_TYPES[value.lower()]
            except KeyError:
                raise ValidationError(self.messages['choices'].format(
                    unicode(self.choices)))

    def to_primitive(self, value, context=None):
        return value.code
