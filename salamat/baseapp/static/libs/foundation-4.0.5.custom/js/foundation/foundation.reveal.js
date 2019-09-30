/*jslint unparam: true, browser: true, indent: 2 */

;(function ($, window, document, undefined) {
  'use strict';

  Foundation.libs.reveal = {
    name: 'reveal',

    version : '4.0.4',

    locked : false,

    settings : {
      animation: 'fadeAndPop',
      animationSpeed: 250,
      closeOnBackgroundClick: true,
      dismissModalClass: 'close-reveal-modal',
      bgClass: 'reveal-modal-bg',
      open: function(){},
      opened: function(){},
      close: function(){},
      closed: function(){},
      bg : $('.reveal-modal-bg'),
      css : {
        open : {
          'opacity': 0,
          'visibility': 'visible',
          'display' : 'block'
        },
        close : {
          'opacity': 1,
          'visibility': 'hidden',
          'display': 'none'
        }
      }
    },

    init : function (scope, method, options) {
      this.scope = scope || this.scope;
      Foundation.inherit(this, 'data_options delay');

      if (typeof method === 'object') {
        $.extend(true, this.settings, method);
      }

      if (typeof method != 'string') {
        if (!this.settings.init) this.events();

        return this.settings.init;
      } else {
        return this[method].call(this, options);
      }
    },

    events : function () {
      var self = this;

      $(this.scope)
        .on('click.fndtn.reveal', '[data-reveal-id]', function (e) {
          e.preventDefault();
          if (!self.locked) {
            self.locked = true;
            self.open.call(self, $(this));
          }
        })
        .on('click.fndtn.reveal touchend.click.fndtn.reveal', this.close_targets(), function (e) {
          if (!self.locked) {
            self.locked = true;
            self.close.call(self, $(this).closest('.reveal-modal'));
          }
        })
        .on('open.fndtn.reveal', '.reveal-modal', this.settings.open)
        .on('opened.fndtn.reveal', '.reveal-modal', this.settings.opened)
        .on('opened.fndtn.reveal', '.reveal-modal', this.open_video)
        .on('close.fndtn.reveal', '.reveal-modal', this.settings.close)
        .on('closed.fndtn.reveal', '.reveal-modal', this.settings.closed)
        .on('closed.fndtn.reveal', '.reveal-modal', this.close_video);
    },

    open : function (target) {
      var modal;

      if (target) {
        modal = $('#' + target.data('reveal-id'));
      } else {
        modal = $(this.scope);
      }

      var open_modal = $('.reveal-modal.open');

      if (!modal.data('css-top')) {
        modal
          .data('css-top', parseInt(modal.css('top'), 10))
          .data('offset', this.cache_offset(modal));
      }

      modal.trigger('open', target);

      if (open_modal.length < 1) {
        this.toggle_bg(modal);
      }

      this.toggle_modals(open_modal, modal);
    },

    close : function (modal) {
      modal = modal || $(this.scope);
      this.locked = true;
      var open_modal = $('.reveal-modal.open').not(modal);
      modal.trigger('close');
      this.toggle_bg(modal);
      this.toggle_modals(open_modal, modal);
    },

    close_targets : function () {
      var base = '.' + this.settings.dismissModalClass;

      if (this.settings.closeOnBackgroundClick) {
        return base + ', .' + this.settings.bgClass;
      }

      return base;
    },

    toggle_modals : function (open_modal, modal) {
      if (open_modal.length > 0) {
        this.hide(open_modal, this.settings.css.close);
      }

      if (modal.filter(':visible').length > 0) {
        this.hide(modal, this.settings.css.close);
      } else {
        this.show(modal, this.settings.css.open);
      }
    },

    toggle_bg : function (modal) {
      if (this.settings.bg.length === 0) {
        this.settings.bg = $('<div />', {'class': this.settings.bgClass})
          .insertAfter(modal);
      }

      if (this.settings.bg.filter(':visible').length > 0) {
        this.hide(this.settings.bg);
      } else {
        this.show(this.settings.bg);
      }
    },

    show : function (el, css) {
      // is modal
      if (css) {
        css.top = $(window).scrollTop() - el.data('offset') + 'px';

        var
          top = $(window).scrollTop() + el.data('css-top'),
          end_css = {
            top: top + 'px',
            opacity: 1
          };

        if (/pop/i.test(this.settings.animation)) {
          return this.delay(function () {
            return el
              .css(css)
              .animate(end_css, this.settings.animationSpeed, function () {
                this.locked = false;
                el.trigger('opened');
              }.bind(this))
              .addClass('open');
          }.bind(this), this.settings.animationSpeed / 2);
        } else {
          css.top = parseInt(top, 10) - 15 + 'px';
        }

        if (/fade/i.test(this.settings.animation)) {
          end_css = {opacity: 1, top: end_css.top};

          return this.delay(function () {
            return el
              .css(css)
              .animate(end_css, this.settings.animationSpeed, function () {
                this.locked = false;
                el.trigger('opened');
              }.bind(this))
              .addClass('open');
          }.bind(this), this.settings.animationSpeed / 2);
        }

        return el.css(css).show().css({opacity: 1}).addClass('open').trigger('opened');
      }

      // should we animate the background?
      if (/fade/i.test(this.settings.animation)) {
        return el.fadeTo(this.settings.animationSpeed / 2, 0.45);
      } else {
        el.css('opacity', 0.45);
      }

      return el.show();
    },

    hide : function (el, css) {
      // is modal
      if (css) {
        var end_css = {
          top: - $(window).scrollTop() - el.data('offset') + 'px',
          opacity: 0
        };

        if (/pop/i.test(this.settings.animation)) {
          return this.delay(function () {
            return el
              .animate(end_css, this.settings.animationSpeed, function () {
                this.locked = false;
                el.css(css).trigger('closed');
              }.bind(this))
              .removeClass('open');
          }.bind(this), this.settings.animationSpeed / 2);
        }

        if (/fade/i.test(this.settings.animation)) {
          end_css = {
            top: parseInt(el.offset().top, 10) + 15 + 'px',
            opacity: 0
          };

          return this.delay(function () {
            return el
              .animate(end_css, this.settings.animationSpeed, function () {
                this.locked = false;
                el.css(css).trigger('closed');
              }.bind(this))
              .removeClass('open');
          }.bind(this), this.settings.animationSpeed / 2);
        }

        return el.hide().css(css).removeClass('open').trigger('closed');
      }

      // should we animate the background?
      if (/fade/i.test(this.settings.animation)) {
        return el.fadeOut(this.settings.animationSpeed / 2);
      }

      return el.hide();
    },

    close_video : function (e) {
      var video = $(this).find('.flex-video'),
          iframe = video.find('iframe');

      if (iframe.length > 0) {
        iframe.attr('data-src', iframe[0].src);
        iframe.attr('src', 'about:blank');
        video.fadeOut(100).hide();
      }
    },

    open_video : function (e) {
      var video = $(this).find('.flex-video'),
          iframe = video.find('iframe');

      if (iframe.length > 0) {
        var data_src = iframe.attr('data-src');
        if (typeof data_src === 'string') {
          iframe[0].src = iframe.attr('data-src');
        }
        video.show().fadeIn(100);
      }
    },

    cache_offset : function (modal) {
      var offset = modal.show().height() + parseInt(modal.css('top'), 10);

      modal.hide();

      return offset;
    },

    off : function () {
      $(this.scope).off('.fndtn.reveal');
    }
  };
}(Foundation.zj, this, this.document));
