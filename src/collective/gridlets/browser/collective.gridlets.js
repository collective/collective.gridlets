/*global console, window, jQuery, document, alert, initTinyMCE */
(function ($) {
    "use strict";

    if ((typeof window.gridlets) === 'undefined') {
        window.gridlets = {};
    }

    var gridlets = window.gridlets;

    gridlets.Gridlets = function (trigger, settings) {
        var self = this;
        self.$trigger = trigger;
        self.columns = self.$trigger.data('gridletsColumns');
        self.min_size = 1;
        $.extend(self, settings);

        self.x_base_dimension = (self.$trigger.width() - 200) / self.columns;
        self.y_base_dimension = (self.$trigger.width() - 200) / (self.columns * 4);
        self.max_cols = self.columns * self.min_size;

        self.$trigger.find('.gridster ul').gridster({
            widget_margins: [10, 10],
            widget_base_dimensions: [
                self.x_base_dimension,
                self.y_base_dimension
            ],
            max_cols: self.max_cols,
            max_size_x: self.max_cols,
            resize: {
                enabled: true,
                min_size: [self.min_size, 1],
                max_size: [self.max_cols, 1],
                axes: ['x'],
                stop: function(e, ui, $widget) {
                    var data = {
                        position: JSON.stringify(this.serialize())
                    };
                    self.$trigger.find('input[type="hidden"]').val(data.position);
                }
            },
            draggable: {
                stop: function(event, ui) {
                    var data = {
                        position: JSON.stringify(this.serialize())
                    };
                    self.$trigger.find('input[type="hidden"]').val(data.position);
                }
            },

            serialize_params: function($w, wgd) {
                return {
                    id: $($w).data().portlethash,
                    col: wgd.col,
                    row: wgd.row,
                    size_x: wgd.size_x,
                    size_y: wgd.size_y
                };
            }
        });
        // var gridster = $(".gridster ul").gridster().data('gridster');

    };

    gridlets.Gridlets.prototype = {

    };

    $.fn.extend({
        gridlets_widget: function (options) {
            return this.each(function () {
                var settings = $.extend(true, {}, options),
                    $this = $(this),
                    data = $this.data('gridlets_widget'),
                    gridlets_widget;

                // If the plugin hasn't been initialized yet
                if (!data) {
                    gridlets_widget = new gridlets.Gridlets($this, settings);
                    $(this).data('gridlets_widget', gridlets_widget);
                }
            });
        }
    });

    $(document).ready(function() {
        $('.gridlets-widget').gridlets_widget();

        // Use bootstrap classes for add portlet dropdown
        $('.template-edit.portaltype-homepage').delegate('#gridportletselector a', 'click', function(event) {
            event.preventDefault();
            event.stopPropagation();
            var $a = $(event.target),
                formfake = $('#portletselectorformfake'),
                newform = "<form id='addgridletform' method='POST' action=''>" +
                       "<input type='hidden' name='referer' value='' />" +
                       "<input type='hidden' name=':action' value='' />" +
                       "</form>",
                $form = $('#addgridletform');

            $('body').append(newform);

            $form.attr('action', formfake.data().action);
            $form.find('input[name=":action"]').val($a.attr('href'));
            $form.find('input[name="referer"]').val(formfake.data().referer);
            $form.submit();
            return false;
        });

        $('.template-edit.portaltype-homepage').delegate('.portlet-action a', 'click', function(event) {
            event.preventDefault();
            event.stopPropagation();
            $('#kss-spinner').show();
            var form = $(this).parents('.portlet-action'),
                data = {};
            data.name = form.data().name;
            data.referrer = form.data().referrer;
            data.viewname = form.data().viewname;
            data._authenticator = form.children('input').val();
            data.ajax = true;
            $.ajax({
                url: form.data().action,
                data: data,
                type: 'POST',
                success: function(data) {
                    if (form.data().friendlyaction === 'delete') {
                        var gridster = $(".gridster ul").gridster().data('gridster');
                        gridster.remove_widget(form.parents('li'));
                        $('#form-widgets-IGridlets-gridlets').val(JSON.stringify(gridster.serialize()));
                    }
                    if (form.data().friendlyaction === 'toggle') {
                        var button = form.children('a'),
                            icon = form.children('a').children('i'),
                            icon_class = icon.attr('class');
                        if (icon_class === 'fa fa-eye') {
                            icon.removeClass('fa-eye');
                            icon.addClass('fa-eye-slash');
                            button.removeClass('btn-success');
                            button.addClass('btn-warning');
                        } else {
                            icon.removeClass('fa-eye-slash');
                            icon.addClass('fa-eye');
                            button.removeClass('btn-warning');
                            button.addClass('btn-success');
                        }
                    }
                    $('#kss-spinner').hide();
                },
                error: function() {
                    $('#kss-spinner').hide();
                }
            });
            return false;
        });

    });

}(jQuery));
