
/*global window, document, console, log*/

/*jshint expr:true*/
!(function($, document, window, undefined) {

    'use strict';

    function init($el, dynamic) {
        // Launches initialization of uploaders.

        if (!$el.data('filesoup')) {
            var
                constructorString = $el.data('uploader'),
                ns = window,
                Constructor;

            try {
                // Try to find uploader constructor in window namespace.
                $.each(constructorString.split('.'), function(i, part) {
                    ns = ns[part];
                    Constructor = ns;
                });
            } catch (e) {}

            if (Constructor) {
                $el.data('filesoup',
                         new Constructor($el, dynamic));
            } else {
                window.console && console.error &&
                    console.error('Could not find upload widget initializer.');
            }
        }
    }

    $(function() {
        $(document.body)
            .on('mouseenter dragenter focus', '[data-uploader]', function() {
                init($(this), true);
            })
            .on('click', '[data-dismiss="upload-alert"]', function() {
                $(this).closest('.alert').slideToggle('fast', function() {
                    $(this).remove();
                });
                return false;
            });

        $('[data-uploader]:visible').each(function() {
            init($(this), false);
        });
    });

})(window.jQuery, document, window);
