"Redactor widget initializer";

/*global _, log, Salamat*/
/*jshint expr:true*/
!(function($, window, document) {
    "use strict";

    $(function() {
        $('[data-redactor-meta]').each(function() {
            var
                $textarea = $(this),
                options = $textarea.data('redactor-meta');

            $textarea.redactor($.extend(options,
                               Salamat.contextData.redactorOptions));
        });
    });

})(window.jQuery, window, document, undefined);
