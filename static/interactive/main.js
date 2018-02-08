//$("#list_of_topics").hide()
$(document).ready(function(){

    

    jQuery.each(jQuery('textarea[data-autoresize]'), function() {

    var offset = this.offsetHeight - this.clientHeight;
     
    console.log("The textarea is seen");


    var resizeTextarea = function(el) {
        jQuery(el).css('height', 'auto').css('height', el.scrollHeight + offset);
    };
    jQuery(this).on('keyup input', function() { resizeTextarea(this); }).removeAttr('data-autoresize');
    });





    // Auto scrollTop 
    $('#chat').scrollTop($('#chat')[0].scrollHeight);


    var roomName = $("#roomName").text();
    var roomAbout = $("#roomAbout").text();

    $("input[id=exampleInputName]").val(roomName);
    $("input[id=exampleInputAbout]").val(roomAbout);






  $('.delete_localchat').unbind("click").click(function(){
      $.ajax({
               type: "POST",
               url: '/m/delete_localchat/',
               data: {'localchat_id': $(this).data('id')},
               dataType: "json",
               success: function(response) {

                  console.log("The localchat was deleted");

                  redirect_url = response.redirect_url;

                  window.location.replace(redirect_url);      





                },
                error: function(rs, e) {
                       alert(rs.responseText);
                }
          });
    }); 


  $('.delete_topic').unbind("click").click(function(){
      $.ajax({
               type: "POST",
               url: '/m/delete_topic/',
               data: {'topic_id': $(this).data('id')},
               dataType: "json",
               success: function(response) {

                  console.log("The topic was deleted");

                  redirect_url = response.redirect_url;

                  window.location.replace(redirect_url);      





                },
                error: function(rs, e) {
                       alert(rs.responseText);
                }
          });
    });      






    $("input[name=modelToSearch]").val("localChat");





    $( "#showTopics" ).click(function() {

        console.log("The showTopics is pressed");

        $("#results").empty(); // empty instead of hiding !!!!!
        $("#results").hide();
        $("#list_of_topics").show()
        $("#list_of_localchats").hide()



        $( "#showLC" ).attr( "class", "" )

        $( "#showT" ).attr( "class", "local_chats_text" )


       $("input[name=modelToSearch]").val("topic");








    });


    $( "#showLocalChats" ).click(function() {

        console.log("The showLocalChats is pressed");

        $("#results").empty();
        $("#results").hide();
        $("#list_of_localchats").show()
        $("#list_of_topics").hide()




        $( "#showT" ).attr( "class", "" )

        $( "#showLC" ).attr( "class", "local_chats_text" )


        $("input[name=modelToSearch]").val("localChat");









    });


    /*
    $("#search_chat_form").submit(function() {




        console.log("The form has been submitted");


        q = $("#q").val();

        modelToSearch = $("#modelToSearch").val();

        console.log(q);
        console.log(modelToSearch);



        $("#list_of_localchats").hide();
        $("#list_of_topics").hide();


        load_resource = $("#load_resource").text() + q + "&modelToSearch=" + modelToSearch

        console.log(load_resource)




        $("#results").load(load_resource);


        return false




    });
    */




// Implement real-time search with keyup function

$('#q').keyup(function (event) {




      $("#list_of_localchats").hide();
      $("#list_of_topics").hide();
      $("#results").show();



      var q = $("#q").val()
      var modelToSearch = $("#modelToSearch").val()
      var chatgroup_id = $("#chatgroup_id").val()

      console.log(modelToSearch)
      console.log(chatgroup_id)



      if (q != '' || query != ' ') {
        $.ajax({
           type: 'GET',
           url: '/m/search_chat_room',
           data: {
             'q': q,
             'modelToSearch': modelToSearch,
             'chatgroup_id': chatgroup_id

           },
           success: function(data) {
              $('#results').html(data);
           },
           error: function(data) {
              console.log(data);
           }
         });
      }
    });




    // Removing the element after search
    // and when user clicked another/outside of this element below.

    $(document).click(function(event) {
      $is_inside = $(event.target).closest('#q').length;

      if( event.target.id == 'q' || $is_inside ) {
        return;
      }else {
        $('#results').empty();
      }
    });





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





$('.messages_wrapper').unbind().on('click', '.like', function(){
      $.ajax({
               type: "POST",
               url: '/m/like/',
               data: {'message_id': $(this).attr('name')},
               dataType: "json",
               success: function(response) {

                      //alert('Company likes count is now ' + response.likes_count);

                      // Update the likes counter
                      message_id = response.message_id
                      console.log(message_id)
                      $("#" + message_id).text(response.likes_count)


                      is_liked = response.is_liked
                      
                      console.log(is_liked)

                      if(is_liked) {

                        $("button[name=" + message_id + "]").find('.fa').attr('class', 'red_heart fa fa-heart');

                        



                      } else {

                        $("button[name=" + message_id + "]").find('.fa').attr('class', 'empty_heart fa fa-heart-o');



                      } 




                  //    $("input[name=" + message_id + "]").val("&#xf259;") // issue with flipping the fa icon

                },
                error: function(rs, e) {
                       alert(rs.responseText);
                }
          });
    });


///$('.like').unbind("click").click()



/*

$('#createLocalChat').submit(function(e) {

    //event.stopPropagation();
    // Work on the file upload, the rest seems to work
    e.preventDefault();

    console.log("A New Local Chat Form has been submitted")
    is_hidden = $("#localChatIsHidden").is(":checked")
    console.log(is_hidden)
    is_private = $('#localChatIsPrivate').is(":checked")
    console.log(is_private)
    //avatar = $("#localChatAvatar").val()
    //console.log(avatar)



    function prepareUpload(event) {

        var files = event.target.files

    }




    $('#localChatAvatar').on('change', prepareUpload);



    console.log(files)


    var filesData = new FormData();
    $.each(files, function(key, value)
    {
        filesData.append(key, value);
    });

    console.log(filesData)





     $.ajax({
               type: "POST",
               url: '/m/new_local_chat/',
               data: {'name': $("#newLocalChatName").val(), 'about': $("#newLocalChatAbout").val(),

               'is_hidden': is_hidden, 'is_private': is_private,

               'avatar': "dick", 'chatgroup_id':$("#chatgroup_id").val()






               },
               dataType: "json",
               processData: false, // Don't process the files
               contentType: false, // Set content type to false as jQuery will tell the server its a query string request
               success: function(response) {

                    console.log("Success")
                    console.log()






                    //window.location.replace('/trending/topics/');


                },
                error: function(rs, e) {
                       alert(rs.responseText);
                }
          });










})
*/

$('body').on('click', '.share', function(e) {

    console.log("The post share button has been clicked")


    $.ajax({
               type: "POST",
               url: '/m/share_post/',
               data: {'message_id': $(this).attr('name')},
               dataType: "json",
               success: function(response) {


                    console.log("Post Successfully shared");

                    var already_posted = response.already_posted;

                    var message_id  = response.message_id

                    console.log(already_posted)

                    if (already_posted) {

                        
                        $("input[name=" + message_id + "]").attr('class', 'share fa');

                    } else {


                         
                         $("input[name=" + message_id + "]").attr('class', 'half_opacity share fa');

                    }





                },
                error: function(rs, e) {
                       alert(rs.responseText);
                }
          });




});

//$('.share').unbind("click").click();


$('.deleteLocalChat').unbind("click").click(function(e) {


    console.log("Deleting the given localchat")


    $.ajax({
               type: "POST",
               url: '/m/delete_localchat/',
               data: {'localchat_id': $(this).attr('name')},
               dataType: "json",
               success: function(response) {


                    localchat_id = response.localchat_id
                    $("#localchat_" + localchat_id).remove()




                },
                error: function(rs, e) {
                       alert(rs.responseText);
                }
          });





});





$(".fav_localchat").unbind("click").click(function(e) {


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











});


