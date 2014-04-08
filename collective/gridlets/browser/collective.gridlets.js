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
      // var form = $(this);
      // var formdata = form.serializeArray();
      // var data = {};
      // for(var i=0; i<formdata.length; i++){
          // data[formdata[i].name] = formdata[i].value;
      // }
      // debugger;
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
                // form.parents('li').remove()
              }
              // container.replaceWith($(data));
              // $('#kss-spinner').hide();
          },
          error: function(){
              // $('#kss-spinner').hide();
          }
      });
      return false;
  });
});
