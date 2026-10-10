import os
from django import template
from django.conf import settings
from django.utils.safestring import mark_safe


# Создаем объект, с помощью которого будем регистрировать собственные теги для шаблонов
register = template.Library()


icons_folder = os.path.join(
    settings.BASE_DIR,
    'static',
    'vendor',
    'tabler',
    'icons'
)

# Создаем собственный тег для вывода иконок в HTML
@register.simple_tag
def tabler_icon(name):

    if not name:
        return ''

    if os.path.basename(name) != name:
        return ''

    icon_path = os.path.join(icons_folder, name + '.svg')

    if not os.path.exists(icon_path):
        return ''

    with open(icon_path, 'r', encoding='utf-8') as file:
        icon_code = file.read()

    # Выводим SVG как HTML-код, чтобы на странице был не обычный текст
    return mark_safe(icon_code)