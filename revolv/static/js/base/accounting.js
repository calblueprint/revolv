$(document).ready(function(){
	//sets up initial values when the page is loaded	
	makeAJAXcall({});
})

$(".selector").change(function(){
	// makes an AJAX call to the accountingJSON view when the selectors are changed
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
});

/**
 * Makes the AJAX Call
 * @param {Object} changed_data - An object with either 0 or 1 keys that maps a selector to its new value.
 */
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

/**
 * Sets the time values, creates column headers, creates row headers, and fills in table values.
 * @param {Object} data - The JSON returned by the AJAX call.
 */
function setValues(data) {
	setTimeValues(data);
	makeColumnHeaders(data);
	makeRowHeaders(data);
	setTableValues(data);
	setTotalsAndCashFlow(data);
}

/**
 * Fills in the appropriate table cells from the given data.
 * @param {Object} data - The JSON returned by the AJAX call.
 */
function setTableValues(data) {
	placeElements(data, 'cash_in', 'donations', placeDonationElement);
	placeElements(data, 'cash_in', 'repayments', placeROIElement);
	placeElements(data, 'cash_in', 'adjustments', placeCashInAdjustmentElement);
	placeElements(data, 'cash_out', 'reinvestments', placeAdminInvestmentElement);
	placeElements(data, 'cash_out', 'adjustments', placeCashOutAdjustmentElement);
}

/**
 * Cleanes up the String to be JQuery friendly.
 * @param {String} text - The text to be cleaned up to be made JQuery friendly.
 */
function cleanUpString(text) {
	text = text.split(' ').join('-').split(';').join('sm').split(":").join('co').split("'").join("ap").split("!").join('ex');
	return text;
}

/**
 * Places a donation element on the page.
 * @param {Object} data_to_insert - A dictionary with values to insert,
 * @param {String} project_name - The name of the project we are inserting under.
 * @param {String} time_key - The time period in which this was inserted.
 */
function placeDonationElement(data_to_insert, project_name, time_key) {
	var total = data_to_insert['total'];
	var payment_service_fees = data_to_insert['payment_service_fees'];
	var retained_donations = data_to_insert['retained_donations'];
	var className  = '.project-' + cleanUpString(project_name);
	$('.total-donation').filter(className).append("<td>" + String(total) + "</td>");
	$('.payment-service-fees').filter(className).append("<td>" + String(payment_service_fees) + "</td>");
	$('.retained-donations').filter(className).append("<td>" + String(retained_donations) + "</td>");
}

/**
 * Places an AdminRepayment element on the page.
 * @param {Object} data_to_insert - A dictionary with values to insert,
 * @param {String} project - The name of the project we are inserting under.
 * @param {String} time - The time period in which this was inserted.
 */
function placeROIElement(data_to_insert, project, time) {
	var total = data_to_insert['total'];
	var revolv_earnings = data_to_insert['revolv_earnings'];
	var retained_ROI = data_to_insert['retained_ROI'];

	var className = '.project-' + cleanUpString(project);
	$('.total-repayment').filter(className).append("<td>" + String(total) + "</td>");
	$('.revolv-earnings').filter(className).append("<td>" + String(revolv_earnings) + "</td>");
	$('.retained-ROI').filter(className).append("<td>" + String(retained_ROI) + "</td>");
}

/**
 * Places an AdminReinvestment element on the page.
 * @param {Object} data_to_insert - A dictionary with values to insert,
 * @param {String} project - The name of the project we are inserting under.
 * @param {String} time - The time period in which this was inserted.
 */
function placeAdminInvestmentElement(data_to_insert, project, time) {
	var total = data_to_insert['total'];

	var className = '.project-' + cleanUpString(project);
	$('.reinvestment').filter(className).append("<td>" + String(total) + "</td>");

}

/**
 * Places a cash in AdminAdjustment element on the page.
 * @param {Object} data_to_insert - A dictionary with values to insert.
 * @param {String} time - The time period in which this was inserted.
 */
var allCashInTransactions = {};
function placeCashInAdjustmentElement(data_to_insert, time) {
	var total = data_to_insert['total'];
	var transactions = data_to_insert['transactions'];

	var allTransactionsKeys = Object.keys(allCashInTransactions);
	for (var i = 0; i < allTransactionsKeys.length; i++) {
		allCashInTransactions[allTransactionsKeys[i]] = 0;
	}
	//insert all the transactions
	var transactionKeys = Object.keys(transactions)
	for (var i = 0; i < transactionKeys.length; i++) {
		var transactionName = transactionKeys[i];
		var transactionAmount = transactions[transactionName];
		var cleanedTransactionName = cleanUpString(transactionName);
		if ($(cleanedTransactionName).length) {
			$('.cash-in-body').append('<tr class="transaction ' + cleanedTransactionName + '"><td>Total</td><td>" + String(total) + "</td></tr>');
		}
		allCashInTransactions[cleanedTransactionName] = transactionAmount;
	}

	allTransactionsKeys = Object.keys(allCashInTransactions);
	for (var i = 0; i < allTransactionsKeys.length; i++) {
		var name = allTransactionsKeys[i];
		var amount = allCashInTransactions[name];
		$('.transaction').filter(name).append("<td>" + amount + "</td>");
	}

	$('.cash-in-adjustment-total').append("<td>" + total + "</td>");
}

/**
 * Places a cash out AdminAdjustment element on the page.
 * @param {Object} data_to_insert - A dictionary with values to insert.
 * @param {String} time - The time period in which this was inserted.
 */
var allCashOutTransactions = {};
function placeCashOutAdjustmentElement(data_to_insert, time) {
	var total = data_to_insert['total'];
	var transactions = data_to_insert['transactions'];

	var allTransactionsKeys = Object.keys(allCashOutTransactions);
	for (var i = 0; i < allTransactionsKeys.length; i++) {
		allCashOutTransactions[allTransactionsKeys[i]] = 0;
	}
	//insert all the transactions
	var transactionKeys = Object.keys(transactions)
	for (var i = 0; i < transactionKeys.length; i++) {
		var transactionName = transactionKeys[i];
		var transactionAmount = transactions[transactionName];
		var cleanedTransactionName = cleanUpString(transactionName);
		if ($(cleanedTransactionName).length) {
			$('.cash-in-body').append('<tr class="transaction ' + cleanedTransactionName + '"><td>Total</td><td>" + String(total) + "</td></tr>');
		}
		allCashInTransactions[cleanedTransactionName] = transactionAmount;
	}

	allTransactionsKeys = Object.keys(allCashOutTransactions);
	for (var i = 0; i < allTransactionsKeys.length; i++) {
		var name = allTransactionsKeys[i];
		var amount = allCashOutTransactions[name];
		$('.transaction').filter(name).append("<td>" + amount + "</td>");
	}

	$('.cash-out-adjustment-total').append("<td>" + total + "</td>");
}

/**
 * Iterates through the data and inserts values onto the page.
 * @param {Object} data - A dictionary of all the data
 * @param {String} cash_in_or_cash_out - 'cash_in' for cash in, and 'cash_out' for cash out.
 */
function placeElements(data, cash_in_or_cash_out, subsection, insert_func) {
	if (subsection == 'adjustments') {
		var super_dict = data[cash_in_or_cash_out][subsection]
		var time_keys = Object.keys(super_dict);
		for (var i = 0; i < time_keys.length; i++) {
			var key = time_keys[i];
			var transactionsAndTotal = super_dict[key];
			insert_func(transactionsAndTotal, key);
		}
	} else {
		var super_dict = data[cash_in_or_cash_out][subsection]
		var time_keys = Object.keys(super_dict);
		for (var i = 0; i < time_keys.length; i++) {
			var key = time_keys[i];
			var project_super = super_dict[key];
			var project_keys = Object.keys(project_super);
			for (var j = 0; j < project_keys.length; j++) {
				var pk = project_keys[j];
				var data_to_insert = project_super[pk];
				insert_func(data_to_insert, pk, key);
			}
		}
	}
}

/**
 * Sets the overal totals and the cash flow values.
 * @param {Object} data - A dictionary with values to insert.
 */
function setTotalsAndCashFlow(data) {
	//create the total row
	//iterate through and create all the cash positions at each time
}

/**
 * Iterates through the 'date_list' list in the data and creates the appropriate column headers.
 * @param {Object} data - The JSON returned by the AJAX call.
 */
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

/**
 * Iterates through the 'project_name' list in the data and creates the appropriate row headers.
 * @param {Object} data - The JSON returned by the AJAX call.
 */
function makeRowHeaders(data) {
	var project_names = data['project_names']
	for (var i = project_names.length-1; i >= 0; i--) {
		var name = cleanUpString(project_names[i]);
		var className = "project-" + name;
		var toAppendInvestment = $('<tr class="reinvestment ' + className + '"><td>' + project_names[i] + '</td></tr>');
		toAppendInvestment.insertAfter(".investment");

		toAppendDonation = $('<tr class = "' + className + '"><td>' + project_names[i] + '</td></tr>' + 
							'<tr class="total-donation ' + className + '"><td>Total</td></tr>' + 
							'<tr class="payment-service-fees ' + className + '"><td>Payment Service Fees</td></tr>' + 
							'<tr class="retained-donations ' + className + '"><td>Retained Donations</td></tr>');

		toAppendDonation.insertAfter('.donation');

		toAppendRepayment = $('<tr><td class="' + className + '">' + project_names[i] + '</td></tr>' + 
							'<tr class="total-repayment ' + className + '"><td>Total</td></tr>' + 
							'<tr class="revolv-earnings ' + className + '"><td>Earnings for RE-volv</td></tr>' + 
							'<tr class="retained-ROI ' + className + '"><td>Retained ROI</td></tr>');

		toAppendRepayment.insertAfter('.ROI');	
	}

	$('.cash-in-body').append('<tr class="cash-in-adjustment-total"><td>Total</td></tr>');
	$('.cash-out-body').append('<tr class="cash-out-adjustment-total"><td>Total</td></tr>');
}

/**
 * Sets the time subtext under the cash flow label using information in the 'date_info' list.
 * @param {Object} data - The JSON returned by the AJAX call.
 */
function setTimeValues(data) {
	//set the time range
	var start_date = parseDate(data['date_info']['start_date']);
	var end_date = parseDate(data['date_info']['end_date']);
	var monthNames = ["January", "February", "March", "April", "May", "June",
	  "July", "August", "September", "October", "November", "December"
	];
	var start_date_string = "" + monthNames[start_date.getMonth()] + " " + start_date.getDate() + ", " + start_date.getFullYear() + " - ";
	var end_date_string = "" + monthNames[end_date.getMonth()] + " " + end_date.getDate() + ", " + end_date.getFullYear();
	$('.time-sub-text').text(start_date_string + end_date_string);
}

/**
 * A helper function that returns a JavaScript Date object from a dateString.
 * @param {String} dateString - A string in the format YYYY-MM-DD representing a date.
 */
function parseDate(dateString) {
	var year = dateString.substring(0, 4);
	var month = String(Number(dateString.substring(5, 7)-1));
	var day = dateString.substring(8, 10);
	return new Date(year, month, day);
}

/**
 * Copied from the Django documentation. Checks if a method needs a csrf token.
 * @param {String} method - The name of a method.
 */
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

/**
 * Copied from the Django documentation. Returns an appropriate cookie.
 * @param {String} name - type of cookie. In this case, we will always use 'csrftoken'.
 */
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