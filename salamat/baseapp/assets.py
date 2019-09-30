
from django_assets import Bundle, register


lib_js = Bundle(
    'libs/jquery-1.8.2.min.js',
    'libs/jquery.easing.1.3.js',
    'libs/underscore.js',
    'js/console.js',
    output='_compress/js/lib.js')

register('lib_js', lib_js)


fresco_js = Bundle(
    'plugins/fresco/fresco.js',
    output='_compress/lightbox/js/lightbox.js')

fresco_css = Bundle(
    'plugins/fresco/fresco.css',
    filters='cssrewrite',
    output='_compress/lightbox/css/lightbox.css')

register('fresco_js', fresco_js)

register('fresco_css', fresco_css)

# register('main_js', Bundle(
#     'js/jquery.min.js',
#     'js/slick.min.js',
#     'plugins/pace/pace.min.js',
#     'js/main.js',
#     output='_compress/js/main.js'))
#
# register('mobile_main_js', Bundle(
#     'mobile/js/jquery.min.js',
#     'mobile/js/slick.min.js',
#     'plugins/pace/pace.min.js',
#     'mobile/js/main.js',
#     output='_compress/js/mobile_main.js'))


register('admin_css', Bundle(
    'css/admin.css',
    filters='cssrewrite',
    output='_compress/admin/css/admin.css'))


register('redactor_js', Bundle(
    'plugins/redactor/redactor.js',
    'plugins/redactor/ru.js',
    'js/redactor.js',
    output='_compress/redactor/js/redactor.js'))


register('redactor_css', Bundle(
    'plugins/redactor/redactor.css',
    filters='cssrewrite',
    output='_compress/redactor/css/redactor.css'))


# register('style_css', Bundle(
#     'css/bootstrap.css',
#     'css/slick.css',
#     'css/style.css',
#     'css/media.css',
#     filters='cssrewrite',
#     output='_compress/css/style.css'))
#
# register('mobile_style_css', Bundle(
#     'mobile/css/bootstrap.css',
#     'mobile/css/slick.css',
#     'mobile/css/style.css',
#     'mobile/css/media.css',
#     filters='cssrewrite',
#     output='_compress/css/mobile_style.css'))