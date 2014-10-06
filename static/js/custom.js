$(document).ready(function() {

	// for persistent cookies
	if ($.cookie('user')) {
		username = $.cookie('user');
		count = $.cookie('count');
		loggedInPage(username, count);
	} else {
		$('#loggedInPage').hide();
	}

	// when user clicks Log In...
	$('#loginButton').click(function() {

	   var username = $('#username').val();
	   var password = $('#password').val();

	   var data = '{"user": "' + username + '", "password": "' + password + '"}';

	   $.ajax({
	   		type: "POST",
	   		url: "users/login",
	   		data: data,
	   		dataType: "json",
	        success: function (response) {
	            if (response.errCode >= 1) {
	            	loggedInPage(username, response.count);
	            	$.cookie('user', username);
	            	$.cookie('count', response.count);
	            } else {
	            	mainPage(response.errCode);
	            }
	        },
	        error: function (xhr, ajaxOptions, thrownError) {
	        alert(xhr.status);
	        alert(thrownError);
	    	}
	   });

	});

	// when users clicks Register...
	$('#registerButton').click(function() {

	   var username = $('#username').val();
	   var password = $('#password').val();

	   var data = '{"user": "' + username + '", "password": "' + password + '"}';

	   $.ajax({
	   		type: "POST",
	   		url: "users/add",
	   		data: data,
	   		dataType: "json",
	        success: function (response) {
	        	debugger
	            if (response.errCode >= 1) {
	            	loggedInPage(username, response.count);
	            	$.cookie('user', username);
	            	$.cookie('count', response.count);
	            } else {
	            	mainPage(response.errCode);
	            }
	        },
	        error: function (xhr, ajaxOptions, thrownError) {
	        alert(xhr.status);
	        alert(thrownError);
	    	}
	   });

	   // alternative way to send requests (for future reference)
	   // $.post( "/users/add", data, function( response ) {
	   //        	if (response.errCode >= 1) {
	   //            	loggedInPage(username, response.count);
	   //            } else {
	   //            	mainPage(response.errCode);
	   //            }
	   // 	},
	   // 	"json"
	   // );

	});

	function mainPage(errCode) {

		ERR_BAD_CREDENTIALS = -1;
		ERR_USER_EXISTS = -2;
		ERR_BAD_USERNAME = -3;
		ERR_BAD_PASSWORD = -4;

	    switch (errCode) {
	    case ERR_BAD_CREDENTIALS:
			$('#vampire img').attr('src', '/media/vampire-badCredentials.png');
	        break;
	    case ERR_USER_EXISTS:
			$('#vampire img').attr('src', '/media/vampire-userExists.png');
	        break;
	    case ERR_BAD_USERNAME:
			$('#vampire img').attr('src', '/media/vampire-badUsername.png');
	        break;
	    case ERR_BAD_PASSWORD:
			$('#vampire img').attr('src', '/media/vampire-badPassword.png');
	        break;
	    }
	}

	function loggedInPage(username, count) {
	  $('#loggedInPage').show();
	  $('.vampire-and-login').hide();

	  if (count == 1) {
	  	$('#successMessage').html("Welcome, " + username + ". You have logged in " + count + " time.");  	
	  } else {
	  	$('#successMessage').html("Welcome, " + username + ". You have logged in " + count + " times.");  	
	  }
	}

	$('#logOut').click(function() {
	  // return to main page
	  $('#loggedInPage').hide();
	  $('.vampire-and-login').show();
	  var imgName = '/media/vampire-default.png';
	  document.getElementById('vampire').innerHTML = '<img src="' + imgName + '" width="279px" height="261px"/>';
	  $.removeCookie('user');
	  $.removeCookie('count');
	});

	$('#username').keyup(function(){
		var usernameInput = $('#username').val();
		if (usernameInput.indexOf('george') > -1 || usernameInput.indexOf('necula') > -1) {
			$('#vampire img').attr('src', '/media/vampire-george.png');
		} else if (usernameInput.indexOf('carina') > -1 || usernameInput.indexOf('boo') > -1) {
			$('#vampire img').attr('src', '/media/vampire-carina.png');
		} else if (usernameInput.indexOf('kevin') > -1 || usernameInput.indexOf('casey') > -1 || usernameInput.indexOf('swag') > -1) {
			$('#vampire img').attr('src', '/media/vampire-kevin.png');
		} else if (usernameInput.indexOf('robin') > -1 || usernameInput.indexOf('kalia') > -1 || usernameInput.indexOf('batman') > -1) {
			$('#vampire img').attr('src', '/media/vampire-robin.png');
		} else {
			$('#vampire img').attr('src', '/media/vampire-default.png');
		}
	});


	// client-side validation

	$('#username').blur(function() {

	   var username = $('#username').val();

	   if (username == '' || username.length > 128) {
	   		$('#vampire img').attr('src', '/media/vampire-badUsername.png');
	   }
	});

	$( "#password" ).blur(function() {

		var password = $('#password').val();

		if (password.length > 128) {
	   		$('#vampire img').attr('src', '/media/vampire-badPassword.png');
	   }
	});

});

