$(".get_user_notifications").click(function(e) {

	// Emptying the contents of the notifications_container

	$('.notifications_container').empty();

	// Getting user's notifications


	$.get('/notify/user_notifications/', function(data) {
       if(data == '') {
          //empty_page = true;
        }
        else {
          //block_request = false;
          $('.notifications_container').append(data);
        }
      });



});


$('body').on('click', '.notification', function() {


  // Empty the current contents of the modal that contains the notification data
  $('.notification_enlarged').empty();

  // First need to figure out the type of the notification

  var notification_type = $(this).data("type");


  // Populate the modal with the respective content depending on the notification type

  if (notification_type=="add_post_comment") {
    


  } else if(notification_type=="like_post_comment") {

  } else if(notification_type=="like_a_message") {



  } else if(notification_type=="like_post") {

    // Need to retreive the specific post that was liked
    var post_id = $(this).data("postid")


    $.get('/notify/single/post/?post_id='+post_id, function(data) {
       if(data == '') {
          //empty_page = true;
        }
        else {
          //block_request = false;
          //$('.notifications_container').append(data);
          $('.notification_enlarged').append(data);
          // now need to display the modal containing the newly fetched data
          $('.notification_enlarged').modal('show');

        }
      });



  }



  



});