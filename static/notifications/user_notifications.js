$(".get_user_notifications").click(function(e) {

	// Emptying the contents of the notifications_container

	$('.notifications_container').empty();

	// Getting user's notifications


	$.get('/notify/user_notifications/', function(data) {
       if(data == '') {
          empty_page = true;
        }
        else {
          block_request = false;
          $('.notifications_container').append(data);
        }
      });



});