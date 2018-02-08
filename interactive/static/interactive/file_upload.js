$( ".chat_image_upload_link" ).click(function(e) {

    e.preventDefault();

    $('.hidden_chat_image_input').trigger('click');
    


});

$(".hidden_chat_image_input").change(function() {

  console.log( "The photo input value was changed" );
  $('.photo_upload_form').one('submit', function(event) {



    event.preventDefault();
    var data = new FormData($('.photo_upload_form').get(0));

    console.log(data);

    $.ajax({
        url: $(this).attr('action'),
        type: $(this).attr('method'),
        data: data,
        cache: false,
        dataType: "json",
        processData: false,
        contentType: false,
        success: function(response) {
            console.log("The photo was successfully uploaded");
            

            message_id = response.message_id;
            console.log(message_id);

            // Here as soon as the message is uploaded
            // we can call the sockets to distributed the
            // photo to the users

            $("#text").val(message_id);
            $("#message_type").val("photo");
            $("#chatform").submit();


            console.log("The chatform has been sumbitted!");




        }
    });
    return false;
    



  });


  $('.photo_upload_form').submit();




});

