
/*global window, document, console*/

/*jshint expr:true*/
!(function($, window, document, undefined) {
    'use strict';

    var CLIPBOARD_FILE_FIELD_NAME = 'clipboard-file';

    // Useful when not using Modernizr;
    $(document.documentElement).addClass('js');

    var MultiUploader = function($el, dynamic) {
        this.init($el, dynamic);
    };

    var SingleUploader = function($el, dynamic) {
        this.init($el, dynamic);
    };

    var __super__ = $.blueimp.fileupload.prototype;

    MultiUploader.prototype = SingleUploader.prototype = {
        init: function($el, dynamic) {
            this.meta = $el.find('[data-meta]').data('meta');
            this.initElements($el, dynamic);
            this.initSlot(dynamic);
            this.initOptions(dynamic);
            this.initFileCount(dynamic);
            this.initThumbnails(this.$files);
            this.initAlerts(dynamic);

// delete this.widgetOptions.acceptFileTypes;
// delete this.widgetOptions.maxFileSize;

            this.initWidget(dynamic);

//console.log(this, this.meta.prefix);
        },

        initElements: function($el) {
            this.$el = $el;
            this.$uploads = $('[data-uploads]', $el);
            this.$files = $('[data-files]', $el);
            this.$totalFilesInput = $('[id$="-TOTAL_FORMS"]', $el);
        },

        initSlot: function() {
            var self = this;

            if (this.meta.prefix === null) {
                this.meta.prefix = this.$el.find('[data-file-input] input[type="file"]').attr('name');
                this.flushClipboard();
            }
        },

        initOptions: function(dynamic) {
            this.widgetOptions = $.extend({
                dropZone: this.$el,
                pasteZone: this.$el,
                filesContainer: this.$uploads,
                downloadFilesContainer: this.$files,
                formData: $.proxy(this.getFormData, this),
                url: this.getUploadURL(dynamic),
                uploadTemplateId: null,
                downloadTemplateId: null,
                uploadTemplate: $.proxy(this.renderUpload, this),
                downloadTemplate: $.proxy(this.renderFile, this)
            }, this.meta.widget.options);
        },

        initFileCount: function() {
            this.totalFiles = this.$files.children().length;
        },

        initThumbnails: function($container) {
            var self = this;

            $container.find('.preview img').each(function() {
                var
                    $img = $(this),
                    $parent = $img.parent(),
                    $thumb = $(new Image()),
                    thumbnailURL = $img.prop('src');

                $thumb.load(function() {
                    self.adjustThumbnailDimensions($thumb, $parent, $img).fadeIn();
                    $thumb.remove();
                });

                $thumb.prop('src', thumbnailURL);
            });
        },

        initWidget: function() {
            "Jquery File Upload plugin initializer";
            var
                self = this,
                widget = this.$el.fileupload(this.widgetOptions).data('fileupload');

            $.extend(widget.options, {
                done: function (e, data) {
                    // This option primarily was overloaded because
                    // JFU doesn't support separate containers for uploaded
                    // and downloaded files.
                    var
                        files = widget._getFilesFromResponse(data),
                        template,
                        deferred;

                    if (data.context) {
                        data.context.each(function (index) {
                            var file = files[index] ||
                                    {error: 'Empty file upload result'},
                                deferred = widget._addFinishedDeferreds();
                            if (file.error) {
                                widget._adjustMaxNumberOfFiles(1);
                            }
                            widget._transition($(this)).done(
                                function () {
                                    template = widget._renderDownload([file])
                                        .appendTo(widget.options.downloadFilesContainer);
                                    widget._forceReflow(template);
                                    widget._transition(template).done(
                                        function () {
                                            data.context = $(this);
                                            widget._trigger('completed', e, data);
                                            widget._trigger('finished', e, data);
                                            deferred.resolve();
                                        }
                                    );
                                }
                            );
                        });
                    } else {
                        if (files.length) {
                            $.each(files, function (index, file) {
                                if (data.maxNumberOfFilesAdjusted && file.error) {
                                    widget._adjustMaxNumberOfFiles(1);
                                } else if (!data.maxNumberOfFilesAdjusted &&
                                        !file.error) {
                                    widget._adjustMaxNumberOfFiles(-1);
                                }
                            });
                            data.maxNumberOfFilesAdjusted = true;
                        }
                        template = widget._renderDownload(files)
                            .appendTo(widget.options.downloadFilesContainer);
                        widget._forceReflow(template);
                        deferred = widget._addFinishedDeferreds();
                        widget._transition(template).done(
                            function () {
                                data.context = $(this);
                                widget._trigger('completed', e, data);
                                widget._trigger('finished', e, data);
                                deferred.resolve();
                            }
                        );
                    }
                },

                fail: function (e, data) {
                    // Here is more correct error handling.
                    // For some reasons JFU doesn't want to treat non-200 response content
                    // as error message; let's fix that. Also add alert when server
                    // is not responding/unreachable.
                    if (data.errorThrown === '' && data.jqXHR.readyState === 0) {
                        data.errorThrown = 'Server is unreachable. Please try again later.';
                    } else if (data.errorThrown !== 'abort' && data.jqXHR.status !== 200) {
                        var response = data.jqXHR.responseText;

                        if (response && response.length && response.length < 140) {
                            // We received some short message about what's going on.
                            data.errorThrown = response;
                        }
                    }

                    return __super__.options.fail.call(this, e, data);
                }
            });

            widget._transition = function ($el) {
                var dfd = $.Deferred();

                if ($el.hasClass('fs-upload')) {
                    return self.animateUpload($el, dfd);
                } else if ($el.hasClass('fs-file')) {
                    return self.animateFile($el, dfd);
                }

                return __super__._transition.call(this, $el);
            };

            this.widget = widget;
        },

        initAlerts: function() {
            "Alert API to deliver messages to user.";

            var $alerts = $('[data-alerts]', this.$el);

            this.alert = function(text, type, method, $container) {
                type = type || 'info';
                method = method || 'appendTo';

                var $alert = $('<div class="alert alert-' + type + '"/>')
                    .append('<a hred="#close" class="close" data-dismiss="upload-alert">&times;</a>')
                    .append(text).hide();

                $alert[method].call($alert, $container || $alerts).slideToggle();
            };
        },

        getUploadURL: function() {
            "Upload url";
            return this.makeURL(this.meta.urls.upload);
        },

        getFormData: function(form) {
            "Default data to be send within an upload request.";

            return [
                {name: 'csrfmiddlewaretoken', value: this.meta.csrftoken}
            ];
        },

        getText: function(text) {
            "i18n support";
            return text;
        },

        getDefaultThumbnailURL: function(file) {
            return 'http://placehold.it/80x80/eeeeee/999999&text=' +
                encodeURIComponent(file.name);
        },

        incFileCount: function() {
            /*jshint plusplus:false*/
            this.totalFiles++;
            this.$totalFilesInput.val(this.totalFiles);
        },

        decFileCount: function() {
            /*jshint plusplus:false*/
            this.totalFiles--;
            this.$totalFilesInput.val(this.totalFiles);
        },

        flushClipboard: function() {
            $.ajax({
                url: this.makeURL(this.meta.urls.clipboard_flush),
                dataType: 'json',
                cache: false
            });
        },

        makeURL: function(pattern, namespace, prefix) {
            "Constructs url from pattern and arguments.";

            namespace = namespace || this.meta.namespace;
            prefix = prefix || this.meta.prefix;
            return pattern
                .replace('__namespace__', namespace)
                .replace('__prefix__', prefix);
        },

        renderUpload: function(data) {
            var
                self = this,
                $files = $();

            $.each(data.files, function (index, file) {
                if (file.error) {
                    self.alert(self.renderFileInfo(file, data), 'error');
                } else {
                    var $file = self.$el
                        .find('[data-templates] [data-template="upload"]')
                        .clone().hide();
                    $file.find('.name').text(file.name);
                    $file.find('.size').text(data.formatFileSize(file.size));
                    $files = $files.add($file);
                }
            });

            return $files;
        },

        renderFile: function(data) {
            var
                self = this,
                $files = $();

            $.each(data.files, function (index, file) {
                if (file.error) {
                    self.alert(self.renderFileInfo(file, data), 'error');
                    return;
                }

                var
                    $file = self.$el
                        .find('[data-templates] [data-template="file"]')
                        .clone().hide(),
                    $preview = $file.find('.preview'),
                    $link = $preview.find('a').attr('href', file.url)
                        .attr('title', file.name);

                $file.find('.name a').text(file.name);

                file.thumbnail_url = file.thumbnail_url ||
                                     self.getDefaultThumbnailURL(file);
                // Actually if your backend is doing well, this code shouldn't
                // reach self.getDefaultThumbnailURL. Genereally it's useful
                // as a fallback during development if something goes wrong.

                self.renderFileThumbnail(file, $link);

                if (file.gallery) {
                    // Is this file of gallery-type, i.e. viewable in lighbox?
                    $link.attr('data-gallery', 'file');
                }

                // Store fid to hidden input.
                $file.find('input[name$="' + CLIPBOARD_FILE_FIELD_NAME + '"]')
                    .val(file.id);

                // Patch $file's DOM by replacing __filesoup_prefix__ with
                // corresponding value in its ids, names and fors attributes.
                $('[id], [name], [for]', $file).each(function() {
                    var
                        $el = $(this),
                        attnames = ['id', 'name', 'for'];

                    // Browse attributes on $el and perform corresponding
                    // replacements.
                    $.each(attnames, function(i, attname) {
                        var attval = $el.attr(attname);
                        if (attval) {
                            var newAttval = attval.replace('__filesoup_prefix__',
                                                           self.totalFiles);
                            if (newAttval !== attval) {
                                $el.attr(attname, newAttval);
                            }
                        }
                    });

                    return $el;
                });

                self.incFileCount();
                $files = $files.add($file);
            });

            return $files;
        },

        renderFileThumbnail: function(file, $link) {
            var
                self = this,
                $thumb = $(new Image());

            $thumb.load(function() {
                $link.removeClass('loading');
                self.adjustThumbnailDimensions($thumb, $link, $thumb)
                    .hide().appendTo($link).fadeIn();
            });

            $link.addClass('loading');
            $thumb.prop('src', file.thumbnail_url).prop('alt', '');
        },

        renderFileInfo: function(file, data) {
            var $info =
                $('<div class="fs-file-info"/>')
                    .append('<div class="error"/>')
                    .append('<div class="name"/>')
                    .append('<div class="size"/>');

            $info.find('.name').html(file.name);
            $info.find('.size').html(data.formatFileSize(file.size));

            if (file.error) {
                $info.find('.error').html(this.getText(file.error));
            }

            return $info;
        },

        animateUpload: function($el, dfd) {
            $el.slideToggle(function() {
                dfd.resolveWith($el);
            });
            return dfd;
        },

        animateFile: function($el, dfd) {
            $el.fadeToggle(function() {
                dfd.resolveWith($el);
            });
            return dfd;
        },

        adjustThumbnailDimensions: function($thumb, $parent, $target) {
            var
                thumb = $thumb.get(0),
                thumbWidth = thumb.width,
                thumbHeight = thumb.height,
                width = $parent.width(),
                height = $parent.height();

            if (thumbWidth > width || thumbHeight > height) {
                // Need resizing.
                var
                    aw = thumbWidth / width,
                    ah = thumbHeight / height;

                if (aw > ah) {
                    thumbHeight = Math.round(thumbHeight / aw);
                    thumbWidth = width;
                } else {
                    thumbWidth = Math.round(thumbWidth / ah);
                    thumbHeight = height;
                }
            }

//console.log(thumbWidth, thumbHeight, width, height);

            return $target.css({
                width: thumbWidth,
                height: thumbHeight,
                marginLeft: -Math.round(thumbWidth / 2),
                marginTop: -Math.round(thumbHeight / 2),
                position: 'absolute',
                top: '50%',
                left: '50%'
            });
        }
    };

    $.filesoup = {
        JFUMultiUploader: MultiUploader,
        JFUSingleUploader: SingleUploader
    };

})(window.jQuery, window, document);


//http://tympanus.net/Tutorials/CSS3Lightbox/index3.html

/////////////////////////////////////////////////////////////////////////////
// DEPRECATED

//function initSingleUpload($upload, __parent__) {
//     var
//         $btn = $upload.find('.fileinput-button'),
//         $thumb = $upload.find('.thumbnail'),
//         $preview = $thumb.find('.preview'),
//         $overlay = $thumb.find('.overlay');

//     $upload.fileupload($.extend({}, {
//         dropZone: $upload,
//         pasteZone: $upload,
//         add: function(e, data) {
//             if ($btn.hasClass('disabled')) {
//                 return false;
//             }
//             data.submit();
//         },
//         start: function() {
//             $btn.addClass('disabled');
//             $overlay.stop().css('opacity', 0).fadeTo(600, 0.6);
//             $thumb.addClass('loading');
//         },
//         success: function(uploads) {
//             $.each(uploads, function(i, upload) {
//                 var $previewItem = $preview.eq(i);
//                 var img = new Image();
//                 $(img).load(function() {
//                     $previewItem
//                         .css('background-image', 'url("' + this.src +'")');
//                     $overlay.stop().fadeOut(800, function() {
//                         $thumb.removeClass('loading');
//                     });
//                 });
//                 img.src = upload.thumbnail_url;
//                 $thumb.removeClass('empty');
//             });
//         },
//         error: function() {
//             $overlay.stop().fadeOut(800, function() {
//                 $thumb.removeClass('loading').addClass('error');
//             });
//         },
//         always: function() {
//             $btn.removeClass('disabled');
//         }
//     }));

//     $upload.bind('fileuploadadd', function(e, data) {
//         if (!$btn.hasClass('disabled')) {
//             $upload.find('.filename').html(data.files[0].name);
//         }
//     });

//     $upload.bind('fileuploadsubmit', function(e, data) {
//         // var formData = $upload.find(':input').serializeArray();
//         // var csrftoken = $upload.closest('form').
//         //     find('input[name="csrfmiddlewaretoken"]').val();
//         // formData.push({name: 'csrfmiddlewaretoken',
//         //               value: csrftoken});
//         // data.formData = formData;
//     });
// }


// Patch this.$el DOM.
// $('[id], [name], [for]', this.$el).each(function() {
//     var
//         $el = $(this),
//         attnames = ['id', 'name', 'for'];

//     $.each(attnames, function(i, attname) {
//         var attval = $el.attr(attname);
//         if (attval) {
//             var newAttval = attval.replace('__uploader_prefix__',
//                                            self.meta.prefix);
//             if (newAttval !== attval) {
//                 $el.attr(attname, newAttval);
//             }
//         }
//     });

//     return $el;
// });
