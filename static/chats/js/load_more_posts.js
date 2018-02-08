// Later on I will combine all the javascript files neatly and then have the if else statements
// likes can be togethter
// infinite scrolls together, etc


// Accessing the url of the page

url = window.location.href.split('/')
console.log(url)

page_name = url[3];
console.log("The page name is "+ page_name);

if (page_name=="recentactivity") {

	console.log("")	


	var page = 1;
  	var empty_page = false;
  	var block_request = false;
   
  $(window).scroll(function() {
  	console.log("recentactivity is scrolled ")
    var margin = $(document).height() - $(window).height() - 250;
    if  ($(window).scrollTop() > margin && empty_page == false && block_request == false) {
     block_request = true;
      page += 1;
      $.get('/load_more_posts/?page='+page, function(data) {
       if(data == '') {
          empty_page = true;
        }
        else {
          block_request = false;
          $('.recent_activity_posts_list').append(data);
        }
      });
    }
  });





}

else {

	;

}


