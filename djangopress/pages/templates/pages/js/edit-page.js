var pageDetailsOpen = false;

function editContentByIdent(event, ident, page) {
	return displayPane(event, {action : 'edit-block', page: page, identifier: ident});
}

function editContentByName(event, name, page) {
	return displayPane(event, {action : 'edit-block', page: page, name: name});
}

function editPage(event, page) {
	return displayPane(event, {action : 'edit-page', page: page});
}

function displayPane(event, data) {
	event.preventDefault();
	if(pageDetailsOpen) {
		$('#page-edit-pane').detach();
	}
	$.ajax({
	      url: '{% url 'page-edit-ajax' %}',
	      type: "GET",
	      data: data,
	      dataType: "html",
	      success: function(msg){
			 $('body').append('<div id="page-edit-pane">' + msg + '</div>');
	         pageDetailsOpen = true;
	         var height = $('#page-edit-pane').height();
	         $('html').css("minHeight", (height + 200) + "px");
	         document.getElementsByTagName("html")[0].scrollTop = 0;
	      }
	   }
	)
	return true;
}