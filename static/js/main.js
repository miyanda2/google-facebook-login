require.config(
{
	shim: 
	{
		'facebook' : 
		{
			exports: 'FB'
		}
	},
	
	paths: 
	{
		"jquery" : "https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min",
		"bootstrap":"https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min",
		"facebook": '//connect.facebook.net/en_US/all',
		"login":"lib/modules/googleFacebook",
		"google" : "https://apis.google.com/js/client:platform"
	}
}
);

require(['jquery'], function() {

	require(['bootstrap'], function() {} );
	require(['login'], function() 
	{
		require(['google'], function() 
		{		
		});

	} );


	require(['facebook'], function()
	{

		window.fbAsyncInit = function() {
		FB.init
		({
			appId      : '296801740840356',
			xfbml      : true,  // parse social plugins on this page
			version    : 'v2.11'
		});
	
		};


	});

});

