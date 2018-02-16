

$('body').on('click', '.post_comment_like_button', function(e) {



console.log("Post comment like button was clicked")


    e.preventDefault();


    $.ajax({
               type: "POST",
               url: '/like_post_comment/',
               data: {'id': $(this).attr('name')},
               dataType: "json",
               success: function(response) {

                      console.log("Success!");



                      is_liked = response.is_liked
                      likes_count = response.likes_count
                      post_comment_id = response.post_comment_id

                      $("#post_comment_" + post_comment_id).text(response.likes_count)

                      if(is_liked) {

                        $("#post_commnet_like_button_"+post_comment_id).find('.fa').attr('class', 'red_heart fa fa-heart');

                      }

                      else {

                        $("#post_commnet_like_button_"+post_comment_id).find('.fa').attr('class', 'empty_heart fa fa-heart-o');

                      }






                },
                error: function(rs, e) {
                       alert(rs.responseText);

                }
          });





});
