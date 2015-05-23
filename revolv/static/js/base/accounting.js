$(document).ready(function(){
	makeAJAXcall({});
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
	setTimeValues(data);
	makeColumnHeaders(data);
	makeRowHeaders(data);
	setTableValues(data);
}

function setTableValues(data) {
	
}

function makeColumnHeaders(data) {
	var shortMonthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
	  "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
	];

	var dates = [];
	var JSONdates = data['date_info']['date_list'];
	for (var i = 0; i < JSONdates.length; i++) {
		var date = parseDate(JSONdates[i]);
		var tableHeader = "" + shortMonthNames[date.getMonth()] + " " + date.getDate();
		var className = "date-" + i;
		var thElement = $('.cash-in-head-row').append('<th class="' + className + '"></th>');
		$("." + className).text(tableHeader);
	}
}

function makeRowHeaders(data) {
	var project_names = data['project_names']
	for (var i = project_names.length-1; i >= 0; i--) {
		var name = project_names[i].replace(" ", "-");
		var className = "project-" + name;
		var toAppend = $('<tr><td class="' + className + '">' + name + '</td></tr>');
		toAppend.insertAfter(".event-type")	
	}
}

function setTimeValues(data) {
	//set the time range
	console.log(data['date_info'])
	var start_date = parseDate(data['date_info']['start_date']);
	var end_date = parseDate(data['date_info']['end_date']);
	console.log(start_date)
	setTimeInformation(start_date, end_date);
}

function parseDate(dateString) {
	var year = dateString.substring(0, 4);
	var month = String(Number(dateString.substring(5, 7)-1));
	var day = dateString.substring(8, 10);
	return new Date(year, month, day);
}

function setTimeInformation(start_date, end_date) {
	var monthNames = ["January", "February", "March", "April", "May", "June",
	  "July", "August", "September", "October", "November", "December"
	];
	var start_date_string = "" + monthNames[start_date.getMonth()] + " " + start_date.getDate() + ", " + start_date.getFullYear() + " - ";
	var end_date_string = "" + monthNames[end_date.getMonth()] + " " + end_date.getDate() + ", " + end_date.getFullYear();
	$('.time-sub-text').text(start_date_string + end_date_string)
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