$(function() {
    let SignUpUsername =  $('#SignUpUsername');
    let SignUpEmail =  $('#SignUpEmail');
    let SignUpPassword = $('#SignUpPassword');
    let SignUpButton = $('SignUpButton');
    let errorUsername = $('#errorUsername');
    let errorEmail = $('#errorEmail');
    let errorPassword = $('#errorPassword');


    $('#SignUpUsername').keyup(function() {
    	console.log("KeyUp");
        $.ajax({
            url: '/SignUpCheck',
            type: 'POST',
            data: {
                "username":$(this).val()
            },
            success: function(response) {
                server_response =  $.parseJSON(response);
                console.log(server_response["status"]);
                username_status = server_response["status"]
                if (username_status == "UsernameExists")
                {
                    error= true;
                    errorUsername.text("Username is already taken")
                }
                else
                {
                    errorUsername.text("")
                }

            },
            error: function(error) {
                console.log(error);
                error = true;
            }
        });
    });


    $('#SignUpEmail').keyup(function() {
        console.log("KeyUp");
        $.ajax({
            url: '/SignUpCheck',
            type: 'POST',
            data: {
                "email":$(this).val()
            },
            success: function(response) {
                server_response =  $.parseJSON(response);
                console.log(server_response["status"]);
                email_status = server_response["status"];
                if (email_status == "EmailExists")
                {
                    error= true;
                    errorEmail.text("Email is already taken");
                }
                else
                {
                    errorEmail.text("");
                }

            },
            error: function(error) {
                console.log(error);
                error = true;
            }
        });
    });


     $('#SignUpPassword').keyup(function() {
        console.log("KeyUp");

        if ($(this).val().match(/^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])([a-zA-Z0-9]{8,})$/)){
            errorPassword.text("");
        }
        else
        {
            errorPassword.text("Password must be at least of 8 Characters, 1 letter, 1 uppercase letter and 1 lowercase letter");
            error = true;
        }

    });

     if ( errorPassword.text()=="" && errorEmail.text()=="" && errorUsername.text()=="" && SignUpUsername.length >0  && SignUpEmail.length>0)
     {
        SignUpButton.attr("disabled","true");
     }

     else
     {
        console.log("Some Error");
        SignUpButton.removeAttr("disabled");        
     }

});


