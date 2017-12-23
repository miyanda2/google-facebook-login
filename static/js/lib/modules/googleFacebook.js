var _token;

function showGoogleSignIn()
{
	//DomAjax
	$.ajax({
			type:'GET',
			url:'/getToken',
			processData: false, // we need dont jquery to process the data into string
			contentType:'application/octet-stream; charaset=utf-8',
			success: function(result,status,xhr)
			{
				// result -> gives what ever was sent from server
				// status is --> success which is obvious given the function was called
				// xhr is like a dict of information for example xhr.responseText == result 				
				
				// ("#demo").html(xhr.responseText); or ("#demo").html(result);
				_token = result
				document.getElementById("googleFacebook").style.zIndex = "5"; 
				$("#googleFacebook").css({"display":"flex"});
				
			}
	});
}
 
function GooglesignInCallback(authResult)
{
	 if (authResult['code'])
	 {
		 

		$.ajax(
		{
			type:'POST',
			url:'/googleSignIn/?token='+_token,
			processData: false, // we need dont jquery to process the data into string
			contentType:'application/octet-stream; charaset=utf-8',
			data:authResult['code'],
			success: function(result,status,xhr)
			{
				if(result)
				{
					HideGoogleFacebook();
					if(result=='False')
					{
						$('#signUpHeader').after('<div class="alert alert-warning"> <strong>New User!</strong> please make account. </div>');
						signUp();
					}
					else
					{
						window.location.href="/";
					}
				}
				else
				{
					alert("Please check your connection! try again");
				}
			}
		
		});
	}
	
}
 
 function HideGoogleFacebook()
 {
	 $("#googleFacebook").css({"display":"none"});
 }
 
  function HideSignUp()
 {
	 $("#signUpDiv").css({"display":"none"});
 }
 
 function signUp()
 {
		// hide login if sign up was clicked from login div footer
		HideGoogleFacebook();
		
	 	document.getElementById("signUpDiv").style.zIndex = "5"; 
		$("#signUpDiv").css({"display":"flex"});
	 
 }

  	
$(document).ready
(
	function()
	{
			
			
		//google 	and facebook
		$('#googleFacebook').on('click', 
		function(e) 
		{
			if (e.target !== this)
				return;
			HideGoogleFacebook();
		});
			
		// signup div
		$('#signUpDiv').on('click', 
		function(e) 
		{
			if (e.target !== this)
					return;
			HideSignUp();
		});
			
		$('.googleFacebookLoginButton').click(
		function ()
		{
			showGoogleSignIn();
		});
			
		$('.signUpButton').click(
		function ()
		{
			signUp();
		});


		$('#login_facebook').click(
		function()
		{ 
			
			FB.login(function(response) 
			{	
				
   			 	if (response.authResponse) 
   			 	{
   			 		//console.log(response);
   				 	facebookSendTokenToServer();
 				}
   			 	else 
   			 	{
     				console.log('User cancelled login or did not fully authorize.');
    			}
			}, {scope: 'user_birthday, user_hometown, user_location, user_photos, user_friends, user_about_me, user_status, email, public_profile, basic_info'});


		});





			
		$('.logout').click(
		function()
		{
			$.ajax(
			{
				type:'GET',
				url:'/logout/',
				contentType:'application/octet-stream; charaset=utf-8',
				success: function(result,status,xhr)
				{
					if(result)
					{
						if(result=='facebook')
						{
							FB.getLoginStatus(
								function(response) 
								{
									if(response.status=='connected')
									FB.logout(function(response)
									{
										console.log("logged out"); 		
		 							});
								})
						}
						window.location.href="/";
					}
				
					else
					{
						alert("Please check your connection! try again");
					}
				}
		
			});



		});


});  
  

    
function facebookSendTokenToServer() 
{
    var access_token = FB.getAuthResponse()['accessToken'];

		$.ajax(
		{
			type: 'POST',
      		url: '/facebookSignIn/?token='+_token,
      		processData: false,
      		data: access_token,
      		contentType: 'application/octet-stream; charset=utf-8',
      		success: function(result) 
      		{
				HideGoogleFacebook();
				if(result=='False')
				{
					$('#signUpHeader').after('<div class="alert alert-warning"> <strong>New User!</strong> please make account. </div>');
					signUp();
				}
				else
				{
					window.location.href="/";
				}
      		}
      
		
	});
 
}
	