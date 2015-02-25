$(function() {
    var projectURL = $('#donation-ajax-js').attr('data-project-url');
    var ffNames = JSON.parse($('#donation-ajax-js').attr('data-field-names'));

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

    /**
     * Generates <ul> for card information. Output should look like this:
     *
     *     Visa ending in 1234
     *     Expires: 05/2020
     *     Name on card: William Taft
     *
     * @param {object} cardInfo - Object with keys from Django
     * CreditCardDonationForm
     */
    var cardInfoBlock = function(cardInfo) {
        var block = $('<ul/>').addClass('confirm-cardInfo-card');
        block.append($('<li/>')
            .text('{0} ending in {1}'.format(
                cardInfo.type.capitalize(), cardInfo.number.substr(-4)
            )));
        block.append($('<li/>')
            .text('Expires: {0}/{1}'.format(
                cardInfo.expire_month, cardInfo.expire_year
            )));
        block.append($('<li/>')
            .text('Name on card: {0} {1}'.format(
                cardInfo.first_name, cardInfo.last_name
            )));
        return block;
    };

    var extraConfirmData = [];
    var $errorList = $('.error-list');
    var $modalErrors = $errorList.parents('.modal-errors');
    $errorList.appendError = function(error) {
        $(this).append($('<li/>').text(error));
    };

    $('#donate-form').submit(function(e) {
        e.preventDefault();
        var form = $(this);
        var formURL = form.attr('action');
        var formData = form.serializeArray();
        $.post(
            projectURL + formURL,
            formData
        ).done(function(data) {
            $errorList.empty();
            $modalErrors.removeClass('error');

            $confirmInfoCard = $('#confirm-info-card');
            $confirmInfoCard.empty();
            $confirmInfoCard.append(cardInfoBlock(data.confirm));

            $('#confirm-info-amount').text('${0} USD'.format(
                (new Number(data.confirm.amount)).toFixed(2)));

            // HACK:
            // manually serializing confirm in Python view to pass to confirm
            // payment modal; not sure if best approach
            extraConfirmData = data.serialized_confirm

            $('#confirm-modal').foundation('reveal', 'open');
        }).fail(function(jqXHR) {
            $errorList.empty();
            $modalErrors.addClass('error');
            if (jqXHR.status != 400) {
                $errorList.appendError('Unknown error. Please try again.');
                return;
            }
            var errors = jqXHR.responseJSON.error;
            for (var i = 0; i < ffNames.length; i++) {
                var fieldName = ffNames[i];
                var field = $('#id_' + fieldName);
                var fieldError = errors[fieldName];
                if (fieldError !== undefined) {
                    field.addClass('error');
                    $errorList.appendError('{0}: {1}'.format(
                        fieldName.capitalize(), fieldError));
                } else {
                    field.removeClass('error');
                }
            }
        });
    });

    $('#change-donation-button').click(function(e) {
        e.preventDefault();
        $('#donate-modal').foundation('reveal', 'open');
    });

    $('#confirm-form').submit(function (e) {
        e.preventDefault();
        var form = $(this);
        var formURL = form.attr('action');
        var formData = form.serializeArray();
        // append card info from validation to this form
        formData.push.apply(formData, extraConfirmData);
        $.post(
            projectURL + formURL,
            formData
        ).done(function(data) {
            $('#amount-donated').text('${0}'.format(
                (new Number(data.amount)).toFixed(2)));
            $('#success-modal').foundation('reveal', 'open');
        }).fail(function(jqXHR) {
            // wat
            alert('Invalid card info. Please re-enter.');
        });
    });
});
