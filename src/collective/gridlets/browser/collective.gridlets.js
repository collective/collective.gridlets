$(document).ready(function() {

  // Use bootstrap classes for add portlet dropdown
  $('.template-edit.portaltype-homepage').delegate('#gridportletselector a', 'click', function(event) {
      event.preventDefault();
      event.stopPropagation();
      $a = $(event.target);
      var formfake = $('#portletselectorformfake');

      var newform = "<form id='addgridletform' method='POST' action=''>" +
                 "<input type='hidden' name='referer' value='' />" +
                 "<input type='hidden' name=':action' value='' />" +
                 "</form>";

      $('body').append(newform);
      $form = $('#addgridletform');
      $form.attr('action', formfake.data().action);
      $form.find('input[name=":action"]').val($a.attr('href'));
      $form.find('input[name="referer"]').val(formfake.data().referer);
      $form.submit();
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
      data['_authenticator'] = form.children('input').val();
      data.ajax = true;
      $.ajax({
          url: form.data().action,
          data: data,
          type: 'POST',
          success: function(data){
              if (form.data().friendlyaction === 'delete'){
                var gridster = $(".gridster ul").gridster().data('gridster');
                gridster.remove_widget(form.parents('li'));
                $('#form-widgets-IGridlets-gridlets').val(JSON.stringify(gridster.serialize()));
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
