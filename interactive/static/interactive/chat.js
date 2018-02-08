// Note that the path doesn't matter right now; any WebSocket
// connection gets bumped over to WebSocket consumers

socket = new ReconnectingWebSocket("wss://" + window.location.host + window.location.pathname);

//var numberOfConnections =

socket.onopen = function(event, message) {

    event.preventDefault()

    console.log("A new connection to the socket is established, the message object is below");
    console.log(message)

    var username = $("#usernameTheRequestUser").val();
    var avatar = $("#avatarOfTheRequestUser").val();
    var room_type = $("input[name='room_type']").val();
    var room_id = $("input[name='room_id']").val();



  

   //data = {'flag':"ws_connect", 'room_type': room_type, 'room_id': room_id}

  // Do the ajax in here to create the flag message
/*

    $.ajax({
               type: "POST",
               url: '/m/new_flag_message/',
               data: {'flag':"ws_connect", 'room_type': $("input[name='room_type']").val(), 'room_id': $("input[name='room_id']").val()},
               dataType: "json",
               success: function(response) {

                  console.log("A new user joined the chat");


                  var message_id = response.message_id;
                  $("#text").val(message_id);
                  $("#message_type").val("flag");
                  $("#chatform").submit();

            

                  console.log("The chatform with the flag has been submitted");      





                },
                error: function(rs, e) {
                       alert(rs.responseText);
                }
          });

*/
/*

    // Add the ability to see the new participants when they connect to the channel later
    var flag_message = JSON.parse(message.data)

    console.log(flag_message)

    // Uppend the flag message in here
    flag_username = flag_message.user
    flag = flag_message.flag
    console.log(flag)


    if(flag=="ws_connect") {
    $flag_message = '<span class="text-center flag_message">' + flag_username + ' has just joined the chat</span>'
     $('#chat').append(


        '<div class="msg">' + $flag_message + '</div>'

);
    

    }


   */





         





    //var data = JSON.parse(message.data);
    console.log("The data has been parsed");

    /*
    if (avatar != "")

    {

    $('.participants').append(


        '<div class="participant"><div class="participant_avatar"><a href="#"><img class="img-circle" src="'+
        avatar+'"height="30px" width="30px"></a></div><div class="participant_info"><a href="#"><span>'+
        username + '</span></a></div><div style="clear:both"> </div><hr><div style="clear:both"> </div></div>'




        )



     }*/
};


socket.onmessage = function(message) {
        event.preventDefault()
        var data = JSON.parse(message.data);
        console.log('the data has been parsed');
        //var avatar = $("#avatarOfTheRequestUser").val()

        // Generating all the necessary variables for the HTML append

        console.log("So, the socket received the reply of the consumer")

        var messageId = data.message_id;
        var numebrOfLikes = data.number_of_likes;
        var message_type = data.message_type;
        console.log(message_type)
        var is_authenticated = true;
        var is_request_user = true;


        

        var like_button_html = '<button type="button" name="'+ messageId + '" class="like fa"> <i class="fa fa-heart-o" aria-hidden="true"></i></button>'
        

        var like_button_html = like_button_html + '<span id="' + messageId + '" style="margin-left: 2px;" class="number_of_likes"> '+
        + numebrOfLikes + '</span>'

        console.log(like_button_html)




        

       

        var share_button_html = '<input type="button" name="' + messageId + '" class="half_opacity share fa" value="&#xf064;" />'

        



        
        


        

         if (message_type=="text") { 

         console.log("Ready to append the text messages!"); 
         $('#chat').append(


        '<div class="msg"> <a class="pull-left"> <img class="img-circle" src="'+ data.profile_avatar  + '" height="40px" width="40px" ></a> <h5><a href="'
         + data.profile_link + '">' + data.user + '</a><span class="time">'+  data.timestamp + '</span></h5><p class="msg_body">'+ data.text + '</span>'
         + like_button_html + share_button_html + '</p></div><div style="clear:both"> </div>'






         );

          } else if(message_type=="photo") {

              console.log("Ready to append the photo message!")

              $('#chat').append(

               '<div class="msg"> <a class="pull-left"> <img class="img-circle" src="'+ data.profile_avatar  + '" height="40px" width="40px" ></a> <h5><a href="'
               + data.profile_link + '">' + data.user + '</a><span class="time">'+  data.timestamp + '</span></h5><p class="msg_body">'+
               '<img class="uploaded_chat_image" src="'+data.photo_url+'">'+ like_button_html + share_button_html+ '</p></div><div style="clear:both"> </div>'

               );
          } else if(message_type=="flag") {
            /*


            console.log("Read to uppend the flag message");

             // Uppend the flag message in here
            flag_username = data.user
            flag = data.flag
            console.log(flag)


            if(flag=="ws_connect") {
            $flag_message = '<span class="text-center flag_message">' + flag_username + ' joined the chat</span>'
             $('#chat').append(


                '<div class="msg">' + $flag_message + '</div>'

            );

            // Appending the new user to the participats section
            
            $('.participants').append(


              '<div class="participant"><div class="participant_avatar"><a href="'+data.profile_link+

              '"><img class="img-circle" src="'+data.profile_avatar+'" height="30px" width="30px"></a></div>'+
              '<div class="participant_info"><a href="'+data.profile_avatar+'"><span>'+data.user+'</span></a></div><div style="clear:both"> </div>'

              )
            

            } else if(flag=="ws_disconnect") {

              $flag_message = '<span class="text-center flag_message">' + flag_username + ' left the chat</span>'
             $('#chat').append(


                '<div class="msg">' + $flag_message + '</div>'

              );



            }

            */
          };

        
        $('#chat').scrollTop($('#chat')[0].scrollHeight);
        $("#message_type").val("text");    










    };





    $("#chatform").on("submit", function(event) {

        event.preventDefault();
        console.log("The button is pressed");
        console.log("Yes, it was submitted, the submit handeler received the message!")
        console.log("The message type is " + $("#message_type").val());
        var message = {
            text: $('#text').val(),
            message_type: $("#message_type").val(),

        }

        console.log("The message variable is ");
        console.log(message)









        if($('#text').val() != '') {



        socket.send(JSON.stringify(message));


            }
        $("#text").val('').focus();



        


        return false;
    });
//});

socket.onclose = function(event, message) {


  console.log("Disconnected from chat socket");
  /*

  $.ajax({
               type: "POST",
               url: '/m/new_flag_message/',
               data: {'flag':"ws_disconnect", 'room_type': $("input[name='room_type']").val(), 'room_id': $("input[name='room_id']").val()},
               dataType: "json",
               success: function(response) {

                  console.log("The user left the chat");


                  var message_id = response.message_id;
                  $("#text").val(message_id);
                  $("#message_type").val("flag");
                  $("#chatform").submit();

            

                  console.log("The chatform with the flag has been submitted");      





                },
                error: function(rs, e) {
                       alert(rs.responseText);
                }
          });


*/
};

