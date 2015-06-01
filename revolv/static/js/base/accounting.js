$(document).ready(function(){
    // sets up initial values when the page is loaded    
    makeAJAXCall({});
})

$(".selector").change(function(){
    // makes an AJAX call to the accountingJSON view when the selectors are changed
    
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
 * Inserts the HTML.
 * @param {Object} data - The HTML returned by the AJAX call.
 */
function setValues(data) {
    $('.table-container').empty();
    $('.table-container').append(data);
}

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