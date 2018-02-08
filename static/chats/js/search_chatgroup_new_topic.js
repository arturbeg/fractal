$('.topic_chatgroup_query').keyup(function(event) {

	$('.chatgroup_search_results').empty();

	event.preventDefault();

	console.log("keyup on the chatgroup query input");

	

	var q = $(this).val();

	$.ajax({
           type: 'GET',
           url: '/chatgroup_search_topic_create/',
           data: {
             'q': q,
           },
           success: function(data) {
              $('.chatgroup_search_results').html(data);
              console.log("The chatgroups were retreived successfully")
           },
           error: function(data) {
              console.log(data);
           }
         });

	$('.chatgroup_search_results').show();
	$('.chatgroup_search_results').dropdown('toggle');




});




$('.chatgroup_search_results').on("click", ".result_item", function(event) {
  
	event.preventDefault();
	console.log("The chatgroup result item has been clicked");
	var chatgroup_id = $(this).data('id');
	console.log("Chatgroup Id is " + chatgroup_id)
	var chatgroup_name = $(this).find('.result_item_name').text();


	
	//$('#chatgroup_query').val(chatgroup_name);
	$('#chatgroup_id').val(chatgroup_id);
	$('.topic_chatgroup_query').text(chatgroup_name);
	$('.topic_chatgroup_query').val(chatgroup_name);
	$('.chatgroup_search_results').hide();


	





});

