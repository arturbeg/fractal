// Sets up the WS for commenting purposes


$('body').on('click', '.load_more_comments', function(e) {

  e.preventDefault()

  console.log("Load more comments was clicked")

  post_id = $(this).data('id')

  console.log("the post id is " + post_id)

  html_post_id = '#post_comments_' + post_id

  var old_number_of_comments = $(html_post_id + ' > *').length;

  console.log(old_number_of_comments)






  

  $.ajax({
               type: "POST",
               url: '/load_more_comments/',
               data: {'id': $(this).data('id'), 'old_number_of_comments': $(html_post_id + ' > *').length},
               dataType: "json",
               success: function(response) {

                  usernames = response.list_of_usernames
                  comment_texts = response.list_of_comment_texts
                  links = response.list_of_links
                  ids = response.list_of_ids
                  list_is_liked = response.list_of_is_liked
                  list_number_of_likes = response.list_number_of_likes


                  
                  // using an inefficient way to create the appends

                  number_of_iterations = usernames.length
                  console.log(number_of_iterations)
                  for(i=0; i<number_of_iterations; i++) {


                    console.log('The comment is liked '+list_is_liked[i] )
                    if (list_is_liked[i]) {   
                      
                      var i_html = '<i class="post_comment_like red_heart fa fa-heart" aria-hidden="true"></i>'

                    }

                    else {

                      var i_html = '<i class="post_comment_like fa fa-heart-o" aria-hidden="true"></i>'   


                    }

                    $('#post_comments_' + post_id).append('<div class="a_comment">'+
                  '<a href="'+ links[i] + '">' + '<span class="username_comment_small">'+
                  usernames[i] + '</span></a>&nbsp<span class="comment_text">'+
                  comment_texts[i]+ '</span>'+


                  '<button id="post_commnet_like_button_'+ids[i]+'" type="button" name="'+ids[i]+
                  '"class="post_comment_like_button fa" >'+i_html+'</button>'+


                  '<span id="post_comment_'+ids[i]+'" style="margin-left: 2px;" class="number_of_likes">'+
                  list_number_of_likes[i]+'</span></div>'



                  )

                    






                  }

                  if(response.no_need_load) {

                    $('#load_more_'+post_id).remove();

                  }
 
                  if(number_of_iterations==0) {

                    console.log("Removing the link");

                    $('#load_more_'+post_id).remove();


                  }
                  



                    




                },
                error: function(rs, e) {
                       alert(rs.responseText);

                }
          });






});


//$('.load_more_comments').unbind("click").click();

$('body').on('submit', '.add_a_comment_form', function(e) {

  e.preventDefault();

  console.log("A comment has been submitted")


  $.ajax({
               type: "POST",
               url: '/add_post_comment/',
               data: {'id': $(this).data('id'), 'comment_text':$(this).find('input[name=comment_text]').val()},
               dataType: "json",
               success: function(response) {


                  console.log("The comment was successfully submitted");


                  username = response.username
                  comment_text = response.comment_text
                  post_id = response.post_id
                  post_comment_id = response.post_comment_id
                  number_of_likes = response.post_comment_number_of_likes
                  var profile_link = response.user_profile_link


                  var post_comment_like_button_html = '<button id="post_commnet_like_button_'+post_comment_id+'" type="button" name="'+post_comment_id+
                  '"class="post_comment_like_button fa" >'+'<i class="post_comment_like fa fa-heart-o" aria-hidden="true"></i>'+'</button>'

                  var span_number_of_likes_html = '<span id="post_comment_'+post_comment_id+'" style="margin-left: 2px;" class="number_of_likes">'+
                  0+'</span>'


                  

                  $('#post_comments_' + post_id).append('<div class="a_comment">'+
                  '<a href="'+ profile_link + '">' + '<span class="username_comment_small">'+
                  username + '</span></a>&nbsp<span class="comment_text">'+
                  comment_text+ '</span>'+


                  '<button id="post_commnet_like_button_'+post_comment_id+'" type="button" name="'+post_comment_id+
                  '"class="post_comment_like_button fa" >'+'<i class="post_comment_like fa fa-heart-o" aria-hidden="true"></i>'+'</button>'+


                  '<span id="post_comment_'+post_comment_id+'" style="margin-left: 2px;" class="number_of_likes">'+
                  number_of_likes+'</span></div>'



                  )


                  number_of_comments = response.number_of_post_comments

                  console.log(number_of_comments)

                  $('#number_of_comments_'+post_id).text(number_of_comments)

                  $('#input_comment_'+post_id).val('')



                },
                error: function(rs, e) {
                       alert(rs.responseText);

                }
          });

});

//$('.add_a_comment_form').on('submit', );
