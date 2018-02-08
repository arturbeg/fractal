// Note that the path doesn't matter right now; any WebSocket
// connection gets bumped over to WebSocket consumers

socket = new ReconnectingWebSocket("wss://" + window.location.host + window.location.pathname);

//var numberOfConnections =

socket.onopen = function(event, message) {

    event.preventDefault()

    console.log("A new connection to the socket is established")

    var username = $("#usernameTheRequestUser").val()
    var avatar = $("#avatarOfTheRequestUser").val()

    

    // Add the ability to see the new participants when they connect to the channel later
    


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







}


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

          } else {

              console.log("Ready to append the photo message!")

              $('#chat').append(

               '<div class="msg"> <a class="pull-left"> <img class="img-circle" src="'+ data.profile_avatar  + '" height="40px" width="40px" ></a> <h5><a href="'
               + data.profile_link + '">' + data.user + '</a><span class="time">'+  data.timestamp + '</span></h5><p class="msg_body">'+
               '<img class="uploaded_chat_image" src="'+data.photo_url+'">'+ like_button_html + share_button_html+ '</p></div><div style="clear:both"> </div>'

               );
          }

        
        $('#chat').scrollTop($('#chat')[0].scrollHeight);
        $("#message_type").val("");    










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




