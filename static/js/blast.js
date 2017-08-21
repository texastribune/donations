
var listen_for_fee_check = function() {
  var fee_checkbox = $('input[name="pay_fees"]');
  var fees_value = $('input[name="pay_fees_value"]');

  fees_value.val("False");

  fee_checkbox.change(function() {
    if ( $(this).is(":checked") ) {
      fees_value.val("True");
    } else if ( $(this).not(":checked") ) {
      fees_value.val("False");
    }
  });
};

// Used to set installments to one for yearly 1-time contributions
var listen_for_installments = function() {
  var openended_status_open = $('input[id="openended_status-0"]');
  var openended_status_none = $('input[id="openended_status-1"]');
  var installments = $('input[name="installments"]');

  // When status is open, installments is always None
  openended_status_open.click(function() {
    installments.val("None");
  });

  // when status is none for yearly members, installments should be 1
  openended_status_none.click(function() {
    installments.val("1");
  });
};

// https://support.stripe.com/questions/can-i-charge-my-stripe-fees-to-my-customers
var payFeeAmount = function() {
  var goalAmount = parseFloat($('input[name="amount"]:checked').val()),
      totalAmount = (goalAmount + .30) / (1 - 0.022);
      feeAmount = Math.floor((totalAmount - goalAmount) * 100) / 100,
      payFeeElement = $('#pay-fee-amount span');

  payFeeElement.text('$' + feeAmount.toFixed(2));
};

$('.subscription > :radio').off('click').on('click', function (e) {
    e.stopPropagation();
});
