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
              var container = form.parents('.portlets-manager');
              container.replaceWith($(data));
              // $('#kss-spinner').hide();
          },
          error: function(){
              // $('#kss-spinner').hide();
          }
      });
      return false;
  });
  // // Call the ws that stores the span value given a portletManager
  // $('.editable').bind('change', function(event) {
  //   // event.preventDefault()
  //   // event.stopPropagation()
  //   data = {'manager': $(this).data()['manager'],
  //           'size': $(this).data()['size'],
  //           'contextId': $(this).data()['contextId'],
  //           'span': $(this).val()};
  //   $.ajax({
  //     url: "@@set-portlethomemanager-span",
  //     data: data,
  //     type: 'POST',
  //     success: function(data){
  //         alertify.success("Configuració guardada.");
  //     },
  //     error: function(){
  //         alertify.error("Error al guardar la configuració.");
  //     }
  //   });
  // });

  // $(".gridster ul").gridster({
  //   widget_margins: [10, 10],
  //   widget_base_dimensions: [140, 140],
  //   max_cols: 6,
  //   resize: {
  //     enabled: true,
  //     axes: ['x'],
  //     stop: function(e, ui, $widget) {
  //       data = {
  //         position: JSON.stringify(this.serialize())
  //       }
  //       $.ajax({
  //         url: document.getElementsByTagName('base')[0].href + "/@@set-portlethomemanager-span",
  //         data: data,
  //         type: 'POST',
  //         success: function(data){
  //             console.log('Guardada!');
  //         },
  //         error: function(){
  //             console.log('Error!');
  //         }
  //       });
  //     }
  //   },
  //   draggable: {
  //     stop: function(event, ui) {
  //       data = {
  //         position: JSON.stringify(this.serialize())
  //       }
  //       $.ajax({
  //         url: document.getElementsByTagName('base')[0].href + "/@@set-portlethomemanager-span",
  //         data: data,
  //         type: 'POST',
  //         success: function(data){
  //             console.log('Guardada!');
  //         },
  //         error: function(){
  //             console.log('Error!');
  //         }
  //       });
  //     }
  //   },
  //   serialize_params: function($w, wgd) {
  //     return {
  //       id: $($w).data().portlethash,
  //       col: wgd.col,
  //       row: wgd.row,
  //       size_x: wgd.size_x,
  //       size_y: wgd.size_y
  //     };
  //   }
  // });

  // var gridster = $(".gridster ul").gridster().data('gridster');
});
