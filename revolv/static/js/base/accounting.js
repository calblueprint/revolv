$(document).ready(function(){
	makeAJAXcall({})
})

$(".selector").change(function(){
		
	var changed_selector = $(this);
	var changed_data = {};

	if (changed_selector.hasClass("start_selector")) {
		changed_data['start_date'] = changed_selector[0].value;
	} else if (changed_selector.hasClass("end_selector")) {
		changed_data['end_date'] = changed_selector[0].value;
	} else {
		changed_data['project_choice'] = changed_selector[0].value;
	}

	makeAJAXcall(changed_data);

	var csrftoken = getCookie('csrftoken');
});

function makeAJAXcall(changed_data) {
	var csrftoken = getCookie('csrftoken');

	$.ajax({
	    url: window.JSONURL,
	    method: "GET",
	    data: changed_data,
	    headers: {"X-CSRFToken": csrftoken},
	    success:function(data, textStatus, xhr){
	    	setValues(data);
	    },
	    error:function (xhr, textStatus, thrownError){
	        alert("Sorry, something went wrong! Try again?");
	    },
	});
}

function setValues(data) {
	//set the time range
	var start_date = parseDate(data['date_info']['start_date']);
	var end_date = parseDate(data['date_info']['end_date']);
}

function parseDate(dateString) {
	var year = Number(dateString.substring(0, 4));
	var month = Number(dateString.substring(5,7));
	var day = Number(dateString.substring(8,10));
	return Date(year, month, day);
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}