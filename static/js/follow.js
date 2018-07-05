$(document).ready( () =>{


	let followUser = $('a');
	console.log(followUser.parent().parent().find(".card-title").text()); 
	followUser.on('click',function (event){
		console.log("Button Clicked");
		let userToFollow=$(this).parent().parent().find(".card-title").text();
		let current_button = $(this);
		$.ajax({
			url:"/follow",
			type:"post",
			data:{
				"userToFollow": userToFollow,
				"followOrUnFollow" : current_button.text()
			},
            success: function(response) {
                server_response =  $.parseJSON(response);
                console.log(server_response["status"]);
                reponse = server_response["status"];
                if (reponse==="followed")
                {
                	current_button.text("Unfollow");
                    current_button.addClass("btn-warning").removeClass("btn-primary");
                }
                else if (reponse=="Unfollowed")
                {
                	current_button.html(` Follow <i class="fa fa-heart" style="font-size:14px" style="color: white;"></i> `);
                      current_button.addClass("btn-primary").removeClass("btn-warning");                  
                }
            },
            error: function(error) {
            	console.log(error);
            }

		});
	})

});