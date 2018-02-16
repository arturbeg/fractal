/*

// Infinite Scrolling for chatgroup topics and localchats
if(chatgroup_topics_displayed) {


console.log("Chatgroup topics displayed");

} 


else {

console.log("Chatgroup localchats displayed");


}

if(chatgroup_topics_displayed) {
  var page_chatgroup_topics = 1;
  var empty_page_chatgroup_topics = false;
  var block_request_chatgroup_topics = false;
  var chatgroup_id = $("input[name=chatgroup_id]").val();
  console.log(chatgroup_id)
   
  $(window).scroll(function() {
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
  });


} else {



  var page_chatgroup_localchats = 1;
  var empty_page_chatgroup_localchats = false;
  var block_request_chatgroup_localchats = false;
  var chatgroup_id = $("input[name=chatgroup_id]").val();
  console.log(chatgroup_id)
   
  $(window).scroll(function() {
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
  });







}





// // Infinite Scrolling for chatgroup topics and localchats

*/