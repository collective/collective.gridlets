$(document).ready(function() {

  // Use bootstrap classes for add portlet dropdown
  $('#portletmanager-collective-gridlets-portletManager').delegate('#gwportletselector a', 'click', function(event) {
    event.preventDefault();
    event.stopPropagation();
    $a = $(event.target);
    // $form = $('form');
    // $form.find('input[name=":action"]').val($a.attr('href'));
    // $form.submit();
        // $('#kss-spinner').show();
        // debugger;
        // var form = $(this);
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
              // debugger;
                var container = form.parents('#content');
                container.replaceWith($('#content', data));

                // $('#kss-spinner').hide();
            },
            error: function(){

                // $('#kss-spinner').hide();
            }
        });
        return false;
  });

  $('.gridster').delegate('.portlet-action a', 'click', function(e){
      event.preventDefault();
      event.stopPropagation();
      // $('#kss-spinner').show();

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
              }
              if (form.data().friendlyaction === 'toggle'){
                icon = form.children('a').children('i')
                icon_class = icon.attr('class');
                if (icon_class === 'fa fa-eye') { icon.removeClass('fa-eye'); icon.addClass('fa-eye-slash');}
                else {icon.removeClass('fa-eye-slash'); icon.addClass('fa-eye');}
              }
          },
          error: function(){
              // $('#kss-spinner').hide();
          }
      });
      return false;
  });
});
