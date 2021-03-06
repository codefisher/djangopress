function startQuickLogin() {
	$("#quick-login-link").click(function( event ) {
		event.preventDefault();
		$("#quick-login-link").hide();
		loadQuickLogin();
	});
}

function loadQuickLogin() {
	$.ajax({
		url: '/accounts/quick_login/',
		type: "GET",
		dataType: "html",
		success: function(data){
			var content = $("#quick-login-content");
			content.empty();
			content.html(data);
			content.show();
			$("#id_username").focus();
			content.click(function(event) {
				if(event.target.id == "quick-login-form") {
					content.empty();
					$("#quick-login-link").show();
				}
			});
		},
		error: function(jqXHR, textStatus, errorThrown){
			$("#quick-login-link").show();
		}
	});
}
