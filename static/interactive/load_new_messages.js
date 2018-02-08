

  var page = 1;
  var empty_page = false;
  var block_request = false;
  var url = window.location.href.split('/');
  var chat_type = url[4];
  console.log(chat_type);
  var chat_label = url[5];
  console.log(chat_label);

  var loading_wheel_src = $('.loading_wheel').attr('src')
  console.log(loading_wheel_src)

  var number_of_pages = parseInt($('#number_of_pages_for_messages').val())
  console.log(number_of_pages)



  $('#chat').scroll(function() { 
    console.log("The chat is being scrolled")
    var margin = $('#chat').height() - 300;
    console.log(margin)
    console.log($("#chat").scrollTop());


    if (page <= number_of_pages) {
      // If scroll top starts here
      if  ($("#chat").scrollTop() < margin && empty_page == false && block_request == false) {

        $('.loading_wheel').remove();
        $('#chat').prepend('<img class="center-block loading_wheel" src="'+loading_wheel_src+'">');       
        block_request = true
        page += 1;
        // generating the get url
        console.log('GETting the rest of the chat messages')
        $.get('/m/load_more_messages/?page=' + page + '&type=' + chat_type + '&label=' + chat_label, function(data) {


         console.log(data)  
         if(data == '') {
            empty_page = true;
          }
          else {
            block_request = false;

            console.log("Scrolltop before " + $("#chat").scrollTop())


            
            $('.loading_wheel').remove();
            
            $('#chat').prepend(data);
            
            
            $('#chat').prepend('<img class="center-block loading_wheel" src="'+loading_wheel_src+'">');
            
            $("#chat").scrollTop(1150);

            console.log("Success in gettig the new messages!")  
          }

          
        });
      }

      // If scrollTop ends here

    } else {

      $('.loading_wheel').remove();
    }
  });




