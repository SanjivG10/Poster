$(function() {
    $('#SignUpUsername').keyup(function() {
    	console.log("KeyUp");
        $.ajax({
            url: '/SignUpCheck',
            type: 'POST',
            data: {
                "username":$(this).val()
            },
            success: function(response) {
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});


