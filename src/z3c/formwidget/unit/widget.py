# -*- coding: utf-8 -*-

# python imports
from pint import UndefinedUnitError
import string

# fanstatic
try:
    from js.bootstrap_select import bootstrap_select
    HAS_BS_SELECT = True
except ImportError:
    HAS_BS_SELECT = False

# zope imports
from z3c.form.widget import FieldWidget
from z3c.form.browser.text import TextWidget
from z3c.form.interfaces import (
    IDataConverter,
    IFieldWidget,
    IFormLayer,
    NO_VALUE,
)
from zope.component import adapter
from zope.interface import (
    implementer,
    implementsOnly,
)
from zope.schema.interfaces import ITextLine

# local imports
from z3c.formwidget.unit import interfaces, ureg, utils
from z3c.formwidget.unit.i18n import _


class MultiUnitWidget(TextWidget):
    """Multi Unit Widget based on TextWidget."""
    implementsOnly(interfaces.IUnitWidget)

    klass = u'multiunit-widget'
    value = u''
    unit = None

    unit_systems = (
        interfaces.SYSTEM_METRIC,
        interfaces.SYSTEM_IMPERIAL,
    )
    preferred_system = interfaces.SYSTEM_METRIC
    level_min = 0
    level_max = None

    data_header = _(u'Select a unit')
    data_width = '75px'

    _javascript_input = """
jQuery(function(jq){
    jq('#${id}-unit').selectpicker({});
});
    """

    @property
    def unit_dimension(self):
        raise NotImplementedError

    @property
    def widget_value(self):
        """Return the converted value."""
        self.unit = self.request.get(self.name + '-unit', self.preferred_unit)
        if not self.value:
            return

        try:
            base_unit = getattr(ureg, self.base_unit)
        except UndefinedUnitError:
            value = self.value
        else:
            # Do the conversion
            converter = IDataConverter(self)
            value = converter.toFieldValue(self.value)
            self.unit = utils.get_best_unit(
                value,
                self.preferred_system,
                self.unit_dimension,
                level_min=self.level_min,
                level_max=self.level_max,
            )
            unit = getattr(ureg, self.unit)
            value = value * base_unit
            value = value.to(unit).magnitude
            value = converter.toWidgetValue(value)
        return value

    def render(self):
        if HAS_BS_SELECT:
            bootstrap_select.need()
        return super(MultiUnitWidget, self).render()

    def extract(self, default=NO_VALUE):
        value = self.request.get(self.name, default)
        unit_name = self.request.get(self.name + '-unit', self.base_unit)
        if unit_name != self.base_unit:
            try:
                unit = getattr(ureg, unit_name)
                base_unit = getattr(ureg, self.base_unit)
            except UndefinedUnitError:
                value = self.field.get(self.context)
            else:
                # Do the conversion
                converter = IDataConverter(self)
                value = converter.toFieldValue(value)
                value = value * unit
                value = value.to(base_unit).magnitude
            value = converter.toWidgetValue(value)
        return value

    def javascript_input(self):
        return string.Template(self._javascript_input).substitute(dict(
            id=self.id,
        ))

    def isSelected(self, key):
        return key == self.unit

    @property
    def base_unit(self):
        raise NotImplementedError

    @property
    def preferred_unit(self):
        return interfaces.UNITS.get(
            self.preferred_system, {}
        ).get(self.unit_dimension, [(None,)])[0][0]

    def items(self):
        items = []
        for system in self.unit_systems:
            dimensions = interfaces.UNITS.get(system, None)
            if not dimensions:
                continue
            units = []
            available_units = dimensions.get(self.unit_dimension, [])
            level_max = self.level_max + 1 if self.level_max else None
            available_units = available_units[self.level_min:level_max]
            for unit in available_units:
                abbr, label_short, label, info = unit
                if abbr is None:
                    # We have a 'level' placeholder.
                    continue
                subtext = label
                if info:
                    subtext = subtext + ' (%s)' % info
                units.append({
                    'id': abbr,
                    'value': abbr,
                    'content': label_short,
                    'subtext': subtext,
                    'selected': self.isSelected(abbr),
                })

            item = {}
            item['title'] = interfaces.LABELS.get(system)
            item['member'] = units
            items.append(item)

        return items


class AreaWidget(MultiUnitWidget):
    """Unit widget for 'area' dimensions."""
    implementsOnly(interfaces.IAreaWidget)
    klass = u'area-widget unit-widget'

    @property
    def unit_dimension(self):
        return interfaces.DIMENSION_AREA

    @property
    def base_unit(self):
        return interfaces.UNIT_SQM[0]


@adapter(ITextLine, IFormLayer)
@implementer(IFieldWidget)
def AreaFieldWidget(field, request):
    """Factory for AreaWidget"""
    return FieldWidget(field, AreaWidget(request))


class LengthWidget(MultiUnitWidget):
    """Unit widget for 'length' dimensions."""
    implementsOnly(interfaces.ILengthWidget)
    klass = u'length-widget unit-widget'

    @property
    def unit_dimension(self):
        return interfaces.DIMENSION_LENGTH

    @property
    def base_unit(self):
        return interfaces.UNIT_M[0]


@adapter(ITextLine, IFormLayer)
@implementer(IFieldWidget)
def LengthFieldWidget(field, request):
    """Factory for LengthWidget"""
    return FieldWidget(field, LengthWidget(request))
