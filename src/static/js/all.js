var display_level = function() {
  var frequency = $('input[name="installment_period"]').val();

  var input_amount = $('input[name="amount"]').val();

  var level_label = $('.level');

  if (frequency == 'monthly') {
    // detemine level and update text based on monthly frequency
    if (input_amount >= 3 && input_amount <= 8) {
      level_label.text('Informed');
    } else if (input_amount >= 9 && input_amount <= 41) {
      level_label.text('Engaged');
    } else if (input_amount >= 42 && input_amount <= 83) {
      level_label.text('Involved');
    } else if (input_amount >= 84 && input_amount <= 208) {
      level_label.text('Editor\'s Circle');
    } else if (input_amount >= 209 && input_amount <= 416) {
      level_label.text('Leadership Circle');
    } else if (input_amount >= 417) {
      level_label.text('Chairman\'s Circle');
    } else {
      level_label.text('');
    }
  } else if (frequency == 'yearly') {
    // detemine level and update text based on yearly frequency
    if (input_amount == 10) {
      level_label.text('Student');
    } else if (input_amount >= 35 && input_amount <= 99) {
      level_label.text('Informed');
    } else if (input_amount >= 100 && input_amount <= 499) {
      level_label.text('Engaged');
    } else if (input_amount >= 500 && input_amount <= 999) {
      level_label.text('Involved');
    } else if (input_amount >= 1000 && input_amount <= 2499) {
      level_label.text('Editor\'s Circle');
    } else if (input_amount >= 2500 && input_amount <= 4999) {
      level_label.text('Leadership Circle');
    } else if (input_amount >= 5000) {
      level_label.text('Chairman\'s Circle');
    } else {
      level_label.text('');
    }
  } else {
    level_label.text('');
    level_label.parent().hide();
  }
};

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
  var installment_period = $('input[name="installment_period"]');

  // When status is open, installments is always None
  openended_status_open.click(function() {
    installments.val("None");
  });

  // when status is none for yearly members, installments should be 1
  // and installment_period should be None
  openended_status_none.click(function() {
    installments.val("1");
    installment_period.val("None");
  });
};

var payFeeAmount = function() {
  var goalAmount = parseFloat($('input[name="amount"]').val());
  var payFeeElement = $('#pay-fee-amount span');

  if (isNaN(goalAmount)) {
    payFeeElement.text('');
  } else {
    // https://support.stripe.com/questions/passing-the-stripe-fee-on-to-customers
    var totalAmount = (goalAmount + .30) / (1 - 0.022);
    // Fee rounded to two decimal places.
    var feeAmount = Math.round((totalAmount - goalAmount) * 100) / 100;

    payFeeElement.text('$' + feeAmount.toFixed(2));
  }
};
