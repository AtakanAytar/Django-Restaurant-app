
	var x= document.getElementById("location");
    function getlocation() {
    	if(navigator.geolocation){
    		navigator.geolocation.getCurrentPosition(showPosition, showError)
    	  }
    	else
    	{
             alert("Sorry! your browser is not supporting")
         } }
     
     function showPosition(position){
       var x =  position.coords.latitude   +"-"    + position.coords.longitude;
                document.getElementById("location").innerHTML = x;
                $.ajax({
                    type: "POST",
                    url: "{{ request.get_full_path }}",
                    data: {
                      'video': x // from form
                    },
                    success: function () {
                      $('#message').html("<h2>Contact Form Submitted!</h2>")
                    }
                  });
               
     }

     function showError(error) {
        switch(error.code){
            case error.PERMISSION_DENIED:
            alert("User denied the request for Geolocation API.");
            break;
        case error.POSITION_UNAVAILABLE:
            alert("USer location information is unavailable.");
            break;
        case error.TIMEOUT:
            alert("The request to get user location timed out.");
            break;
        case error.UNKNOWN_ERROR:
            alert("An unknown error occurred.");
            break;
    }
        }
