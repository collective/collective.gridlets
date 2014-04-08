$(document).ready(function() {

  // Use bootstrap classes for add portlet dropdown
  $('.template-edit.portaltype-homepage').delegate('#gridportletselector a', 'click', function(event) {
      event.preventDefault();
      event.stopPropagation();
      $a = $(event.target);
      var form = $('#portletselectorform');
      var data = {};
      data[':action'] = $a.attr('href');
      data['referer'] = form.data().referer

      data.ajax = true;
      $.ajax({
          url: form.data().action,
          data: data,
          type: 'POST',
          success: function(data){
              var container = form.parents('#content');
              container.replaceWith($('#content', data));
              $('.gridster ul').gridster({
                  widget_margins: [10, 10],
                  widget_base_dimensions: [150, 150],
                  max_cols: 6,
                  resize: {
                    enabled: true,
                    axes: ['x'],
                    stop: function(e, ui, $widget) {
                      data = {
                        position: JSON.stringify(this.serialize())
                      }
                      $('#form-widgets-IGridlets-gridlets').val(data.position);
                    }
                  },
                  draggable: {
                    stop: function(event, ui) {
                      data = {
                        position: JSON.stringify(this.serialize())
                      };
                      $('#form-widgets-IGridlets-gridlets').val(data.position);
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
              $('#kss-spinner').hide();
          },
          error: function(){
              $('#kss-spinner').hide();
          }
      });
      return false;
  });

  $('.template-edit.portaltype-homepage').delegate('.portlet-action a', 'click', function(e){
      event.preventDefault();
      event.stopPropagation();
      $('#kss-spinner').show();
      var form = $(this).parents('.portlet-action');
      var data = {};
      data['name'] = form.data().name;
      data['referrer'] = form.data().referrer;
      data['viewname'] = form.data().viewname;
      data['_authenticator'] = form.children('input').val()
      data.ajax = true;
      $.ajax({
          url: form.data().action,
          data: data,
          type: 'POST',
          success: function(data){
              if (form.data().friendlyaction === 'delete'){
                var gridster = $(".gridster ul").gridster().data('gridster');
                gridster.remove_widget(form.parents('li'));
                $('#form-widgets-IGridlets-gridlets').val(JSON.stringify(gridster.serialize()))
              }
              if (form.data().friendlyaction === 'toggle'){
                button = form.children('a');
                icon = form.children('a').children('i');
                icon_class = icon.attr('class');
                if (icon_class === 'fa fa-eye') {
                  icon.removeClass('fa-eye'); icon.addClass('fa-eye-slash');
                  button.removeClass('btn-success'); button.addClass('btn-warning');
                }
                else {
                  icon.removeClass('fa-eye-slash'); icon.addClass('fa-eye');
                  button.removeClass('btn-warning'); button.addClass('btn-success');
                }
              }
              $('#kss-spinner').hide();
          },
          error: function(){
              $('#kss-spinner').hide();
          }
      });
      return false;
  });
});
