$(document).ready(function(){


// Read more of the post

$('body').on('click', '.display_rest_of_post', function(event) {

  event.preventDefault();
  $.ajax({
               type: "GET",
               url: '/post_more/',
               data: {'id': $(this).data('id')},
               dataType: "json",
               success: function(response) {

                      console.log("Successfully got the rest of the text")
                      var full_text = response.full_text;
                      console.log(full_text)
                      var post_id = response.post_id
                      // Delete the more button



                      $('#user_message_'+post_id).html(full_text)




                },
                error: function(rs, e) {
                       alert(rs.responseText);

                }
          });



});










$('.upload_chatgroup_photo').unbind("click").click(function(event) {

  event.preventDefault();
  $('#id_avatar').trigger('click');

});

$('#id_avatar').change(function(event) {


var filename = $(this).val().replace(/C:\\fakepath\\/i, '');   
$('.photo_location').text(filename);

});



  // Choosing a custom class for the paragraph on 
  // the sing in page

  
  




  var chatgroup_topics_displayed = true;

console.log("The webpage is loaded")



url = window.location.href.split('/')
console.log(url)

page_type = url[3];
console.log("The page type is "+ page_type);


if (page_type=="trending") {
// Infinite Scrolling for trending

  console.log("Infinite Scrolling func for a trending page")
  

  var page = 1;
  var empty_page = false;
  var block_request = false;
   
  $(window).scroll(function() {
    var margin = $(document).height() - $(window).height() - 250;
    if  ($(window).scrollTop() > margin && empty_page == false && block_request == false) {
     block_request = true;
      page += 1;
      $.get('/trending/topics/data/?page=' + page, function(data) {
       if(data == '') {
          empty_page = true;
        }
        else {
          block_request = false;
          $('.posts_container').append(data);
        }
      });
    }
  });







// Infinite Scrolling for trending
}

// Displaying the users who liked a post

$('body').on('click', '.show_who_liked', function(event) {

  event.preventDefault();

  // Empty the contents of the modal first

  $('.post_likers').empty();
  $('.profile_modal').empty();

  post_id = $(this).data('id');

  $.get('/load_post_likers/'+post_id + '/', function(data) {

    // Load the html into the modal

    $('.post_likers').append(data);

    // Now show the modal

    $('.post_likers').modal('show');


  });



});



//$('.show_who_liked').unbind('click').click();



// Displaying the users who liked a post


$('.show_modal').unbind("click").click(function(event) {

  event.preventDefault();
  $('.profile_modal').empty();
  $('.post_likers').empty();
  profile_id = $(this).data('id');
  console.log("the profile id is "+profile_id)

  if ($(this).hasClass('show_followers_modal')) {
  $.get('/u/'+profile_id+'/followers/', function(data) {

    console.log("Locating the followers")

    $('.profile_modal').append(data);
    $('.profile_modal').modal('show');


  });

  } else if ($(this).hasClass('show_following_modal'))  {

    $.get('/u/'+profile_id+'/following/', function(data) {

    $('.profile_modal').append(data);
    $('.profile_modal').modal('show');


  });


  };


});


// Displaying following and followers


  


//





// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');




function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});


$(".input_link").unbind("click").click(function(e) {

  e.preventDefault();

  post_id = $(this).data('id');


  $("#input_comment_"+post_id).focus();

});



// There double fav_localchat, needs to be fixed

$('body').on('click', '.fav_localchat', function(e) {


    e.preventDefault();

    console.log("Localchat Fav button pressed in the related section");


    $.ajax({
               type: "POST",
               url: '/fav_localchat/',
               data: {'id': $(this).data('id')},
               dataType: "json",
               success: function(response) {

                      console.log("It worked");
                      console.log(response.number_of_participants);
                      var localchat_id = response.localchat_id;
                      var is_fav = response.is_fav
                      console.log("is_fav " + is_fav)


                      $("#number_of_favs_"+localchat_id).text(response.number_of_participants);
                      $("#number_of_favs_r_"+localchat_id).text(response.number_of_participants);
                      console.log(localchat_id)

                      if(is_fav) {

                        $('#localchat_button_'+localchat_id).attr('class', 'fav_button fav_localchat');
                        $('#localchat_button_r_'+localchat_id).attr('class', 'fav_button fav_localchat');
                      }

                      else {

                        $('#localchat_button_'+localchat_id).attr('class', 'fav_button_pale fav_localchat');
                        $('#localchat_button_r_'+localchat_id).attr('class', 'fav_button_pale fav_localchat');

                      }



                },
                error: function(rs, e) {
                       alert(rs.responseText);

                }
          });







});


//$(".fav_localchat").unbind("click").click();







$("body").on('click', '.post_like_button', function(e) {


console.log("Liking or Disliking a post")


    e.preventDefault();


    $.ajax({
               type: "POST",
               url: '/like_post/',
               data: {'id': $(this).attr('name')},
               dataType: "json",
               success: function(response) {

                      console.log("The post was successfully liked or the like was successfully removed")



                      is_liked = response.is_liked
                      likes_count = response.likes_count
                      post_id = response.post_id

                      $("#" + post_id).text(response.likes_count)

                      if(is_liked) {

                        $("button[name=" + post_id + "]").find('.fa').attr('class', 'red_heart fa fa-heart');

                      }

                      else {

                        $("button[name=" + post_id + "]").find('.fa').attr('class', 'empty_heart fa fa-heart-o');

                      }






                },
                error: function(rs, e) {
                       alert(rs.responseText);

                }
          });





});


//$(".post_like_button").unbind("click").click()
















$('body').on('click', '.afollow', function(e) {


console.log("Follow/Unfollow")


    e.preventDefault();


    $.ajax({
               type: "POST",
               url: '/chatgroup_follow/',
               data: {'id': $(this).data('id')},
               dataType: "json",
               success: function(response) {

                      console.log("It worked")
                      var follower_counter = response.num_followers
                      console.log(follower_counter)

                      $("#follower_counter").text(follower_counter)

                      console.log(response.is_following)

                      if (response.is_following) {

                        $(".afollow").text("Unfollow")


                      }

                      else {

                        $(".afollow").text("Follow")

                      }





                },
                error: function(rs, e) {
                       alert(rs.responseText);

                }
          });





} );



// Unvbind click can be a thing that fixes double click
//$(".afollow").unbind("click").click()






$(".afollow_search_list").unbind("click").click(function(e) {


console.log("Follow/Unfollow")


    e.preventDefault();


    $.ajax({
               type: "POST",
               url: '/chatgroup_follow/',
               data: {'id': $(this).data('id')},
               dataType: "json",
               success: function(response) {

                      chatgroup_id = response.chatgroup_id

                      console.log("It worked")
                      var follower_counter = response.num_followers
                      console.log(follower_counter)

                      $("#follower_counter" + chatgroup_id).text(follower_counter)

                      console.log(response.is_following)

                      if (response.is_following) {

                        $("#follow_big" + chatgroup_id).text("Unfollow")
                        $("#follow_small" + chatgroup_id).text("Unfollow")


                      }

                      else {

                        $("#follow_big" + chatgroup_id).text("Follow")
                        $("#follow_small" + chatgroup_id).text("Follow")

                      }





                },
                error: function(rs, e) {
                       alert(rs.responseText);

                }
          });





})





/*

$(".follow_chatgroup").click(function(){


    $.post('/chatgroup/followit/', {'chatgroup_id': $(this).attr('name')}, function(data) {

        console.log("Success");


    }, "json");


});

*/


$('body').on('click', '.raise_topic', function(e) {


    console.log("Raise a topic")

    e.preventDefault();




    $.ajax({
               type: "POST",
               url: '/raise_topic/',
               data: {'id': $(this).data('id')},
               dataType: "json",
               success: function(response) {

                      console.log("It worked");
                      console.log(response.topic_rating)
                      var topic_id = response.topic_id
                      var rating = response.topic_rating
                      $("#" + topic_id).text(rating);
                      $("#r_" + topic_id).text(rating)

                      is_raised = response.is_raised

                      if(is_raised) {

                      $("#up_" + topic_id).attr('class', 'red small_arrow raise_topic')
                      $("#down_" + topic_id).attr('class', 'small_arrow lower_topic')


                      $("#up_r_" + topic_id).attr('class', 'red small_arrow raise_topic')
                      $("#down_r_" + topic_id).attr('class', 'small_arrow lower_topic')

                    } else {

                      $("#up_" + topic_id).attr('class', 'small_arrow raise_topic')
                      $("#up_r_" + topic_id).attr('class', 'small_arrow raise_topic')

                    }



                },
                error: function(rs, e) {
                       alert(rs.responseText);

                }
          });







});

//$(".raise_topic").unbind("click").click()


$('body').on('click', '.lower_topic', function(e) {


    console.log("Lower a topic")

    e.preventDefault();

    

    $.ajax({
               type: "POST",
               url: '/lower_topic/',
               data: {'id': $(this).data('id')},
               dataType: "json",
               success: function(response) {

                      console.log("It worked");
                      console.log(response.topic_rating)
                      var topic_id = response.topic_id
                      var rating = response.topic_rating
                      $("#" + topic_id).text(rating)
                      $("#r_" + topic_id).text(rating)


                      is_lowered = response.is_lowered

                      if(is_lowered) {

                      $("#down_" + topic_id).attr('class', 'black small_arrow lower_topic')
                      $("#up_" + topic_id).attr('class', 'small_arrow raise_topic')

                      $("#down_r_" + topic_id).attr('class', 'black small_arrow lower_topic')
                      $("#up_r_" + topic_id).attr('class', 'small_arrow raise_topic')

                    } else {

                      $("#down_" + topic_id).attr('class', 'small_arrow lower_topic')
                      $("#down_r_" + topic_id).attr('class', 'small_arrow lower_topic')

                    }



                },
                error: function(rs, e) {
                       alert(rs.responseText);

                }
          });




});


//$(".lower_topic").unbind("click").click()



$("#display_chatgroup_localchats").unbind("click").click(function(e) {


    e.preventDefault();

    console.log("Display Localchats Clicked")

    $("#topics_select_span").attr('class', 'select1')
    $("#localchats_select_span").attr('class', 'select2')

    $(".chatgroup_localchats").css('display', 'block')
    $(".chatgroup_topics").css('display', 'none')

    chatgroup_topics_displayed = false;






})


$("#display_chatgroup_topics").unbind("click").click(function(e) {


    e.preventDefault();

    console.log("Display Topics Clicked")

    $("#topics_select_span").attr('class', 'select2')
    $("#localchats_select_span").attr('class', 'select1')

    $(".chatgroup_localchats").css('display', 'none')
    $(".chatgroup_topics").css('display', 'block')


    chatgroup_topics_displayed = true;







});


$('body').on('click', '.add_top_fav', function(e) {


    e.preventDefault();

    console.log("Localchat Fav button pressed");


    $.ajax({
               type: "POST",
               url: '/fav_localchat/',
               data: {'id': $(this).data('id')},
               dataType: "json",
               success: function(response) {

                      console.log("It worked");
                      console.log(response.number_of_participants);
                      var localchat_id = response.localchat_id;



                      $("#number_of_favs_"+localchat_id).text(response.number_of_participants)



                },
                error: function(rs, e) {
                       alert(rs.responseText);

                }
          });







});

//$(".add_to_fav").unbind("click").click();
$('body').on('click', '.follow_a_user', function(e) {



    $.ajax({
               type: "POST",
               url: '/follow_a_user/',
               data: {'id': $(this).data('id')},
               dataType: "json",
               success: function(response) {

                      console.log("It worked");
                      var number_of_followers = response.number_of_followers
                      var profile_id = response.profile_id
                      console.log(profile_id)


                      $("#profile_id_" + profile_id).text(number_of_followers)

                      is_following = response.is_following

                      console.log(is_following)

                      if (is_following) {

                            

                            $("#follow_a_user_"+profile_id).text("Unfollow");
                            $("#follow_a_user_small_"+profile_id).text("Unfollow");

                      }

                      else  {


                            
                            $("#follow_a_user_"+profile_id).text("Follow");
                            $("#follow_a_user_small_"+profile_id).text("Follow");

                      };





                },
                error: function(rs, e) {
                       alert(rs.responseText);

                }
          });




});

//$(".follow_a_user").unbind("click").click()










/*
$(".editProfile").submit(function(e) {

    console.log("The form has been submitted")



    $.ajax({
               type: "POST",
               url: '/edit/',
               data: {'id': $(this).attr('id'), "about": $("#editAbout").val(), "username": $("#editUsername").val()},
               dataType: "json",
               success: function(response) {

                      console.log("It worked")

                      //userURL = $("#userURL").val()

                      //window.location.href(userURL)


                },

                error: function(rs, e) {
                       alert(rs.responseText);

                }
          });











})

*/



// Infinite Scrolling for chatgroup topics and localchats
var page_chatgroup_localchats = 1;
var empty_page_chatgroup_localchats = false;
var block_request_chatgroup_localchats = false;
var chatgroup_id = $("input[name=chatgroup_id]").val();

var page_chatgroup_topics = 1;
var empty_page_chatgroup_topics = false;
var block_request_chatgroup_topics = false;


console.log(chatgroup_topics_displayed)
 
  
   
  $(window).scroll(function() {

    if(chatgroup_topics_displayed) {
    console.log("Scrolling chatgroup topics")
    var margin_c_t = $(document).height() - $(window).height() - 250;
    if  ($(window).scrollTop() > margin_c_t && empty_page_chatgroup_topics == false && block_request_chatgroup_topics == false) {
     block_request_chatgroup_topics = true;
      page_chatgroup_topics += 1;
      $.get('/chat_group_topics_more/'+chatgroup_id+'/?page=' + page_chatgroup_topics, function(data) {
       if(data == '') {
          empty_page_chatgroup_topics = true;
        }
        else {
          block_request_chatgroup_topics = false;
          $('.chatgroup_topics').append(data);
        }
      });
    }

    }


    else {


      console.log("Scrolling chatgroup localchats")
      var margin_c_l = $(document).height() - $(window).height() - 250;
    if  ($(window).scrollTop() > margin_c_l && empty_page_chatgroup_localchats == false && block_request_chatgroup_localchats == false) {
     block_request_chatgroup_localchats = true;
      page_chatgroup_localchats += 1;
      $.get('/chat_group_localchats_more/'+chatgroup_id+'/?page=' + page_chatgroup_localchats, function(data) {
       if(data == '') {
          empty_page_chatgroup_localchats = true;
        }
        else {
          block_request_chatgroup_localchats = false;
          $('.chatgroup_localchats').append(data);
        }
      });
    }





    }
  });







});