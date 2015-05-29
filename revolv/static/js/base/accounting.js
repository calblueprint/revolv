$(document).ready(function(){
    // sets up initial values when the page is loaded    
    makeAJAXCall({});
})

$(".selector").change(function(){
    // makes an AJAX call to the accountingJSON view when the selectors are changed
    
    $(".added").remove();
    var changedSelector = $(this);
    var changedData = {};

    if (changedSelector.hasClass("start_selector")) {
        changedData['start_date'] = changedSelector[0].value;
    } else if (changedSelector.hasClass("end_selector")) {
        changedData['end_date'] = changedSelector[0].value;
    } else {
        changedData['project_choice'] = changedSelector[0].value;
    }
    makeAJAXCall(changedData);
});

/**
 * Makes the AJAX Call
 * @param {Object} changed_data - An object with either 0 or 1 keys that maps a selector to its new value.
 */
function makeAJAXCall(changedData) {
    var csrftoken = getCookie('csrftoken');

    $.ajax({
        url: window.JSONURL,
        method: "GET",
        data: changedData,
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
    var newText = "";
    for (var i = 0; i < text.length; i++) {
        var value = text.charCodeAt(i);
        if (value < 65 || value > 122) {
            newText += 'z';
        } else {
            newText = text.charAt(i);
        }
    }
    return newText;
}

/**
 * Places a donation element on the page.
 * @param {Object} data_to_insert - A dictionary with values to insert,
 * @param {String} project_name - The name of the project we are inserting under.
 * @param {String} time_key - The time period in which this was inserted.
 */
function placeDonationElement(dataToInsert, projectName, timeKey) {
    var total = dataToInsert['total'];
    var paymentServiceFees = dataToInsert['payment_service_fees'];
    var retainedDonations = dataToInsert['retained_donations'];
    var className  = '.project-' + cleanUpString(projectName);
    $('.total-donation').filter(className).append('<td class="added">' + total + "</td>");
    $('.payment-service-fees').filter(className).append('<td class="added">' + paymentServiceFees + "</td>");
    $('.retained-donations').filter(className).append('<td class="added">' + retainedDonations + "</td>");
}

/**
 * Places an AdminRepayment element on the page.
 * @param {Object} data_to_insert - A dictionary with values to insert,
 * @param {String} project - The name of the project we are inserting under.
 * @param {String} time - The time period in which this was inserted.
 */
function placeROIElement(dataToInsert, project, time) {
    var total = dataToInsert['total'];
    var revolvEarnings = dataToInsert['revolv_earnings'];
    var retainedROI = dataToInsert['retained_ROI'];

    var className = '.project-' + cleanUpString(project);
    $('.total-repayment').filter(className).append('<td class="added">' + total + "</td>");
    $('.revolv-earnings').filter(className).append('<td class="added">' + revolvEarnings + "</td>");
    $('.retained-ROI').filter(className).append('<td class="added">' + retainedROI + "</td>");
}

/**
 * Places an AdminReinvestment element on the page.
 * @param {Object} data_to_insert - A dictionary with values to insert,
 * @param {String} project - The name of the project we are inserting under.
 * @param {String} time - The time period in which this was inserted.
 */
function placeAdminInvestmentElement(dataToInsert, project, time) {
    var total = dataToInsert['total'];

    var className = '.project-' + cleanUpString(project);
    $('.reinvestment').filter(className).append('<td class="added">' + total + "</td>");

}

/**
 * Places a cash in AdminAdjustment element on the page.
 * @param {Object} data_to_insert - A dictionary with values to insert.
 * @param {String} time - The time period in which this was inserted.
 */
var allCashInTransactions = {};
function placeCashInAdjustmentElement(dataToInsert, time) {
    var total = dataToInsert['total'];
    var transactions = dataToInsert['transactions'];

    var allTransactionsKeys = Object.keys(allCashInTransactions);
    for (var i = 0; i < allTransactionsKeys.length; i++) {
        allCashInTransactions[allTransactionsKeys[i]] = 0;
    }
    // insert all the transactions
    var transactionKeys = Object.keys(transactions)
    for (var i = 0; i < transactionKeys.length; i++) {
        var transactionName = transactionKeys[i];
        var transactionAmount = transactions[transactionName];
        var cleanedTransactionName = cleanUpString(transactionName);
        allCashInTransactions[cleanedTransactionName] = transactionAmount;
    }
    
    allTransactionsKeys = Object.keys(allCashInTransactions);
    for (var i = 0; i < allTransactionsKeys.length; i++) {
        var name = allTransactionsKeys[i];
        var amount = allCashInTransactions[name];
        $('.transaction').filter('.' + name).append('<td class="added">' + amount + "</td>");
    }

    $('.cash-in-adjustment-total').append('<td class="added">' + total + "</td>");
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
    // insert all the transactions
    var transactionKeys = Object.keys(transactions)
    for (var i = 0; i < transactionKeys.length; i++) {
        var transactionName = transactionKeys[i];
        var transactionAmount = transactions[transactionName];
        var cleanedTransactionName = cleanUpString(transactionName);
        allCashOutTransactions[cleanedTransactionName] = transactionAmount;
    }
    
    allTransactionsKeys = Object.keys(allCashOutTransactions);
    for (var i = 0; i < allTransactionsKeys.length; i++) {
        var name = allTransactionsKeys[i];
        var amount = allCashOutTransactions[name];
        $('.transaction').filter('.' + name).append('<td class="added">' + amount + "</td>");
    }

    $('.cash-out-adjustment-total').append('<td class="added">' + total + "</td>");
}

/**
 * Iterates through the data and inserts values onto the page.
 * @param {Object} data - A dictionary of all the data
 * @param {String} cash_in_or_cash_out - 'cash_in' for cash in, and 'cash_out' for cash out.
 * @param {String} subsection - either 'adjustments', 'donations', 'repayments', or 'reinvestments'
 * @param {function} insertFunc - the respective function that inserts this into the DOM
 */
function placeElements(data, cashInOrCashOut, subsection, insertFunc) {
    if (subsection == 'adjustments') {
        var superDict = data[cashInOrCashOut][subsection]
        var timeKeys = Object.keys(superDict);
        timeKeys.sort();
        for (var i = 0; i < timeKeys.length; i++) {
            var key = timeKeys[i];
            var transactionsAndTotal = superDict[key];
            insertFunc(transactionsAndTotal, key);
        }
    } else {
        var superDict = data[cashInOrCashOut][subsection]
        var timeKeys = Object.keys(superDict);
        timeKeys.sort();
        for (var i = 0; i < timeKeys.length; i++) {
            var key = timeKeys[i];
            var projectSuper = superDict[key];
            var projectKeys = Object.keys(projectSuper);
            for (var j = 0; j < projectKeys.length; j++) {
                var pk = projectKeys[j];
                var dataToInsert = projectSuper[pk];
                insertFunc(dataToInsert, pk, key);
            }
        }
    }
}

/**
 * Sets the overal totals and the cash flow values.
 * @param {Object} data - A dictionary with values to insert.
 */
function setTotalsAndCashFlow(data) {
    // create the total row
    // iterate through and create all the cash positions at each time
    $('.cash-in-body').append('<tr class="added level-0 total-cash-in"><td class="level-0 added">Total Cash In</td><tr>');
    $('.cash-out-body').append('<tr class="added level-0 total-cash-out"><td class="level-0 added">Total Cash Out</td><tr>');

    $('.cash-flow-table').append('<tbody class="added cash-position"></tbody>');
    $('.cash-position').append('<tr class="added initial-cash-position"><td class="level-0 added">Initial Cash Position</td></tr>');
    $('.cash-position').append('<tr class="added net-cash"><td class="level-0 added">Net Change in Cash</td></tr>');
    $('.cash-position').append('<tr class="added final-cash-position"><td class="level-0 added">Final Cash Position</td></tr>');

    var cashPositions = data['cash_balances'];
    var dateKeys = Object.keys(cashPositions);
    dateKeys.sort();
    for (var i = 0; i < dateKeys.length; i++) {
        var key = dateKeys[i];
        var cashInfo = cashPositions[key];
        var initialCash = cashInfo['beginning_cash_balance'];
        var changeInCash = cashInfo['change_in_cash'];
        var finalCash = cashInfo['final_cash_balance'];
        var netCashIn = cashInfo['net_cash_in'];
        var netCashOut = cashInfo['net_cash_out'];
        $('.initial-cash-position').append('<td class="added">' + initialCash + '</td>');
        $('.net-cash').append('<td class="added">' + changeInCash + '</td>');
        $('.final-cash-position').append('<td class="level-0 table-content added">' + finalCash + '</td>');
        $('.total-cash-in').append('<td class="level-0 table-content added">' + netCashIn + '</td>');
        $('.total-cash-out').append('<td class="level-0 table-content added">' + netCashOut + '</td>');
    }
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
        var thElement = $('.cash-in-head-row').append('<th class="added ' + className + '"></th>');
        $("." + className).text(tableHeader);
    }
}

/**
 * Iterates through the 'project_name' list in the data and creates the appropriate row headers.
 * @param {Object} data - The JSON returned by the AJAX call.
 */
function makeRowHeaders(data) {
    var projectNames = data['project_names']
    var tableWidth = data['date_info']['date_list'].length;
    for (var i = projectNames.length-1; i >= 0; i--) {
        var name = cleanUpString(projectNames[i]);
        var className = "project-" + name;
        var toAppendInvestment = $('<tr class="added reinvestment ' + className + '"><td class="level-1 added">' + projectNames[i] + '</td></tr>');
        toAppendInvestment.insertAfter(".investment");

        toAppendDonation = $('<tr class = "added project-donation ' + className + '"><td class="level-1 added">' + projectNames[i] + '</td></tr>' + 
                            '<tr class="added total-donation ' + className + '"><td class="level-2 added">Total</td></tr>' + 
                            '<tr class="added payment-service-fees ' + className + '"><td class="level-2 added">Payment Service Fees</td></tr>' + 
                            '<tr class="added retained-donations ' + className + '"><td class="level-2 added">Retained Donations</td></tr>');

        toAppendDonation.insertAfter('.donation');

        toAppendRepayment = $('<tr class="added project-repayment"><td class="level-1 added ' + className + '">' + projectNames[i] + '</td></tr>' + 
                            '<tr class="added total-repayment ' + className + '"><td class="level-2 added">Total</td></tr>' + 
                            '<tr class="added revolv-earnings ' + className + '"><td class="level-2 added">Earnings for RE-volv</td></tr>' + 
                            '<tr class="added retained-ROI ' + className + '"><td class="level-2 added">Retained ROI</td></tr>');

        toAppendRepayment.insertAfter('.ROI');  
    }

    for (var i = 0; i < tableWidth; i++) {
        $('.project-donation').append('<td class="added"></td>');
        $('.project-repayment').append('<td class="added"></td>');
        $('.other-type').append('<td class="added"></td>');
        $('.event-type').append('<td class="added"></td>');
        $('.cash-out-head-row').append('<th class="added"></th>');
    }
    
    var inNames = data['cash_in_adjustment_names']
    for (var i = 0; i < inNames.length; i++) {
        var name = inNames[i];
        var cleanedName = cleanUpString(name);
        $('.cash-in-body').append('<tr class="added transaction ' + cleanedName + '"><td class="level-2 added">'+ name +'</td></tr>');
        allCashInTransactions[cleanedName] = 0;
    }
    
    var outNames = data['cash_out_adjustment_names']
    for (var i = 0; i < outNames.length; i++) {
        var name = outNames[i];
        var cleanedName = cleanUpString(name);
        $('.cash-out-body').append('<tr class="added transaction ' + cleanedName + '"><td class="level-2 added">'+ name +'</td></tr>');
        allCashOutTransactions[cleanedName] = 0;
    }

    $('.cash-in-body').append('<tr class="added cash-in-adjustment-total"><td class="level-0 added">Total</td></tr>');
    $('.cash-out-body').append('<tr class="added cash-out-adjustment-total"><td class="level-0 added">Total</td></tr>');
}

/**
 * Sets the time subtext under the cash flow label using information in the 'date_info' list.
 * @param {Object} data - The JSON returned by the AJAX call.
 */
function setTimeValues(data) {
    // set the time range
    var startDate = parseDate(data['date_info']['start_date']);
    var endDate = parseDate(data['date_info']['end_date']);
    var monthNames = ["January", "February", "March", "April", "May", "June",
      "July", "August", "September", "October", "November", "December"
    ];
    var startDateString = "" + monthNames[startDate.getMonth()] + " " + startDate.getDate() + ", " + startDate.getFullYear() + " - ";
    var endDateString = "" + monthNames[endDate.getMonth()] + " " + endDate.getDate() + ", " + endDate.getFullYear();
    $('.time-sub-text').text(startDateString + endDateString);
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