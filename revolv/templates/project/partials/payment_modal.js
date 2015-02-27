{% load tojson %}

$(function() {


if (!String.prototype.format) {
    /**
     * Python style string formatting for Javascript Strings.
     * (http://stackoverflow.com/questions/610406)
     *
     *     '{0} {1}'.format('Hello', 'world!') --> 'Hello world!'
     */
    String.prototype.format = function() {
        var args = arguments;
        return this.replace(/{(\d+)}/g, function(match, number) {
            return typeof args[number] != 'undefined' ? args[number] : match;
        });
    };
}
if (!String.prototype.capitalize) {
    /**
     * Capitalizes every word in string, replacing underscore with spaces.
     *
     *     'hello_world!' --> 'Hello World!'
     */
    String.prototype.capitalize = function() {
        return this.replace(/_/g, ' ')
            .replace(/\w\S*/g, function(txt) {
                return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
            });
    }
}

var validObj = {
    'cc-number': false,
    'cc-expiry': false,
    'cc-cvc': false,
    'cc-name': false,
    'donation-amount': false
}
var validForm = function() {
    var validForm = true;
    $.each(validObj, function(k, v) {
        if (!v) { validForm = false; return false; }
    });
    return validForm;
};
var getDonateFormValues = function() {
    var formValues = {};
    $.each($('#donate-form').serializeArray(), function(i, field) {
        formValues[field.name] = field.value;
    });
    return formValues;
}
donationContinueBtnDOM = $('button.donation-continue')[0];
donationContinueBtnDOM.disabled = true;

/**
 * Adds class 'error' to inputEle if validFunc returns false on
 * varArgs. Updates validObj as well, and will toggle the disabled state
 * on the donation form Continue button as a side-effect.
 *
 * @param {String} fieldName - Name of field to update in validObj
 * @param {jQuery Element} inputEle - Element to apply class to
 * @param {function} validFunc - Function that operates on varArgs
 * @param {anything} varArgs - Arbitrary arguments to pass to validFunc
 */
var validOrApplyErrorClass = function(fieldName, inputEle, validFunc, varArgs) {
    validObj[fieldName] =
        validFunc.apply(this, Array.prototype.slice.call(arguments, 3));
    inputEle.toggleClass(
        'error',
        !validObj[fieldName]
    );
    donationContinueBtnDOM.disabled = !validForm();
};

$ccNumber = $('input.cc-number');
$ccNumber.payment('formatCardNumber');

var activeCardType = null;
var $activeTypeEle = null;
$ccNumber.keyup(function() {
    var cardType = $.payment.cardType(this.value);
    if (cardType != null) {
        if (activeCardType != cardType && $activeTypeEle != null) {
            $activeTypeEle.removeClass('active');
        }
        $activeTypeEle = $('img.cc-type-{0}'.format(cardType)).addClass('active');
    } else if ($activeTypeEle != null) {
        $activeTypeEle.removeClass('active');
        $activeTypeEle = null;
    }
    activeCardType = cardType;
});
$ccNumber.blur(function() {
    validOrApplyErrorClass(
        'cc-number',
        $ccNumber,
        $.payment.validateCardNumber,
        this.value
    );
});

$ccExpiry = $('input.cc-expiry');
$ccExpiry.payment('formatCardExpiry');
$ccExpiry.blur(function() {
    var expiryVal = $.payment.cardExpiryVal(this.value);
    validOrApplyErrorClass(
        'cc-expiry',
        $ccExpiry,
        $.payment.validateCardExpiry,
        expiryVal.month,
        expiryVal.year
    );
});

$ccCVC = $('input.cc-cvc');
$ccCVC.payment('formatCardCVC');
$ccCVC.blur(function() {
    validOrApplyErrorClass(
        'cc-cvc',
        $ccCVC,
        $.payment.validateCardCVC,
        this.value,
        activeCardType
    );
});

$ccName = $('input.cc-name');
$ccName.blur(function() {
    var verifyFirstLast = function(fullName) {
        var split = fullName.split(' ');
        if (split.length != 2) { return false; }
        var e;
        for (var i = 0; i < split.length; i++) {
            e = split[i];
            if (e == null || e.length == 0) { return false; }
        }
        return true;
    };
    validOrApplyErrorClass(
        'cc-name',
        $ccName,
        verifyFirstLast,
        this.value
    );
});

$donationAmount = $('input.donation-amount');

/**
 * Ripped and modified from Stripe jQuery.payment source. Formats
 * the input field to always be of the form "$ 20" or "$ 20.00".
 * (https://github.com/stripe/jquery.payment/blob/master/src/jquery.payment.coffee)
 */
$donationAmount.keypress(function(e) {
    // Key event is for a browser shortcut
    if (e.metaKey || e.ctrlKey) {
        return true;
    }
    // If keycode is a space
    if (e.which == 32) {
        return false;
    }
    // If keycode is a special char (WebKit)
    if (e.which == 0) {
        return true;
    }
    // If char is a special char (Firefox)
    if (e.which < 33) {
        return true;
    }

    input = String.fromCharCode(e.which);
    var val = $donationAmount.val();

    // If val is empty, make sure first char is a number
    if (val == '') {
        var validInput = /[1-9]/.test(input);
        if (!validInput) {
            return false;
        }
        e.preventDefault();
        setTimeout(function() {
            $donationAmount.val('$ {0}'.format(input));
        });
    } else {
        // Else, get just the decimal amount and do error checking there
        var decimalVal = val.slice(2)
        if (/^\d+\.\d*$/.test(decimalVal) && !/[\d]/.test(input)) {
            return false;
        } else if (/^\d+$/.test(decimalVal) && !/[\d\.]/.test(input)) {
            return false;
        }
        e.preventDefault();
        setTimeout(function() {
            $donationAmount.val('$ {0}{1}'.format(decimalVal, input));
        });
    }
});
/**
 * Handles backspace logic for decimal dollars value field.
 * (https://github.com/stripe/jquery.payment/blob/master/src/jquery.payment.coffee)
 */
$donationAmount.keydown(function(e) {
    var value = $donationAmount.val();

    // Return unless backspacing
    if (e.which != 8) {
        return;
    }

    var selectionStart = $donationAmount.prop('selectionStart');
    var selectionEnd = $donationAmount.prop('selectionEnd');
    if (selectionStart != null && selectionEnd != null &&
        selectionStart < 4) {

        e.preventDefault();
        if (value.length == 3) {
            setTimeout(function() {
                $donationAmount.val('');
            });
            return;
        }

        var newVal = value.slice(selectionEnd);
        if (newVal == '') {
            setTimeout(function() {
                $donationAmount.val('');
            });
        } else {
            if (newVal[0] == '.') {
                newVal = newVal.slice(1);
            }
            setTimeout(function() {
                $donationAmount.val('$ {0}'.format(newVal));
            });
        }
    }
});

/**
 * Validates decimal dollars value field when user clicks away from input.
 * (https://github.com/stripe/jquery.payment/blob/master/src/jquery.payment.coffee)
 */
$donationAmount.blur(function() {
    var validAmount = function(amountStr) {
        return /^\d+(\.\d{2})?$/.test(amountStr);
    };
    validOrApplyErrorClass(
        'donation-amount',
        $donationAmount,
        validAmount,
        this.value.slice(2)
    );
});

var populateConfirmModal = function(formValues) {
    $confirmInfoCard = $('.confirm-info-card');
    $confirmInfoCard.find('.type').text(activeCardType.capitalize());
    $confirmInfoCard.find('.lastfour').text(formValues['cc-number'].slice(-4));
    $confirmInfoCard.find('.expiry').text(formValues['cc-expiry']);
    $confirmInfoCard.find('.name').text(formValues['cc-name']);

    $('span.confirm-info-amount').text('{0} USD'.format(
        formValues['donation-amount']));
};
$('button.donation-continue').click(function(e) {
    e.preventDefault();
    populateConfirmModal(getDonateFormValues());
    $('#confirm-modal').foundation('reveal', 'open');
});
$('button.donation-change').click(function(e) {
    e.preventDefault();
    $('#donate-modal').foundation('reveal', 'open');
});
$('button.donation-submit').click(function(e) {
    e.preventDefault();
    $('#donate-form').submit();
});
$donateModalErrors = $('#donate-modal').find('.modal-errors');

/**
 * CreditCardDonationForm fields:
 *
 * csrfmiddlewaretoken (csrf token)
 * first_name
 * last_name
 * type (of card)
 * number (of card)
 * expire_month
 * expire_year
 * cvv2
 * amount
 */
$('#donate-form').submit(function(e) {
    e.preventDefault();
    if (!validForm()) { return false; }
    var form = $(this);

    var formValues = getDonateFormValues();
    var nameSplit = formValues['cc-name'].split(' ');
    var expiryVal = $.payment.cardExpiryVal(formValues['cc-expiry']);
    var creditCardDonationFormData = [{
        'name': 'csrfmiddlewaretoken',
        'value': formValues['csrfmiddlewaretoken']
    }, {
        'name': 'first_name',
        'value': nameSplit[0]
    }, {
        'name': 'last_name',
        'value': nameSplit[1]
    }, {
        'name': 'type',
        'value': activeCardType
    }, {
        'name': 'number',
        'value': formValues['cc-number'].replace(/\s/g, '')
    }, {
        'name': 'expire_month',
        'value': expiryVal.month
    }, {
        'name': 'expire_year',
        'value': expiryVal.year
    }, {
        'name': 'cvv2',
        'value': formValues['cc-cvc']
    }, {
        'name': 'amount',
        'value': formValues['donation-amount'].slice(2)
    },
    ];

    var formURL = form.attr('action');

    $.post(
        '/project/{{ project.pk }}/' + formURL,
        creditCardDonationFormData
    ).done(function(data) {
        $donateModalErrors.removeClass('error');
        $('#amount-donated').text('${0}'.format(
            (new Number(data.amount)).toFixed(2)));
        $('#success-modal').foundation('reveal', 'open');
    }).fail(function(jqXHR) {
        $donateModalErrors.addClass('error');
        $donateModalErrors.children('.error-msg')
            .text('Your card information is invalid. Please correct it.');
        $('#donate-modal').foundation('reveal', 'open');
    });

});


});
