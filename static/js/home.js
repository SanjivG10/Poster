$(document).ready(function(){


	$('.notificationLink').on('click',function(){

		console.log("Clicked");
		$('.no_notification').css('display','none');

	});

   $('#dropdownMenuButton').on('click',function(){
        console.log("You clicked me");
        $.ajax({
            url:"/updateLastSeen",
            type:"post",
            data:{
                "time": "update"  
            },
            success: function(reponse)
            {
                console.log("I am ok");
            },
            error: function(error) {
                console.log(error);
            }
        });
    });

   if ($('.no_notification').text() < 1)
   {
   		$('.no_notification').css("display","none");
   }



});