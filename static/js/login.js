$(function() {
    let SignUpUsername =  $('#SignUpUsername');
    let SignUpEmail =  $('#SignUpEmail');
    let SignUpPassword = $('#SignUpPassword');
    let SignUpButton = $('#SignUpButton');
    let errorUsername = $('#errorUsername');
    let errorEmail = $('#errorEmail');
    let errorPassword = $('#errorPassword');
    errorPassword.text("The password is weak");

    var testEmail = /^[A-Z0-9._%+-]+@([A-Z0-9-]+\.)+[A-Z]{2,4}$/i;



    $('#SignUpUsername').keyup(function() {
    	console.log("KeyUp");
        checkButton();
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
                    checkButton();  
                }
                else
                {
                    if (SignUpUsername.val().match(/^[a-zA-Z0-9.\-_$@*!]{3,15}$/))
                    {
                        errorUsername.text("");
                    }
                    else
                    {
                        errorUsername.text("Username is not valid. It must be 3 character at least and 15 characters at  max");    
                    }
                }

            },
            error: function(error) {
                console.log(error);
                error = true;
                checkButton();     
            }
        });
    });


    $('#SignUpEmail').keyup(function() {
            
        checkButton();

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
                        error = true;
                        checkButton();
     
                }

            },
            error: function(error) {
                console.log(error);
                error = true;
                checkButton();
            }
        });
    });


     $('#SignUpPassword').keyup(function() {
        checkButton();
        if ($(this).val().match(/^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])([a-zA-Z0-9]{8,})$/)){
            errorPassword.text("");
        }
        else
        {
            errorPassword.text("Password must be at least of 8 Characters, 1 letter, 1 uppercase letter and 1 lowercase letter");
            error = true;
            checkButton();
        }

    });

    var checkButton  =  function(){

         if ( errorPassword.text()=="" && errorEmail.text()=="" && errorUsername.text()=="" && SignUpEmail.val()!="" && SignUpPassword.val()!="" && SignUpUsername.val()!="")
         {
            console.log("No Error");
            SignUpButton.removeAttr("disabled");
         }

         else
         {
            console.log("Some Error");
            SignUpButton.attr("disabled","true");
         }


    }



});


