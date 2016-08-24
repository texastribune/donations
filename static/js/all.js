var display_level = function() {
  var frequency = $('input[name="installment_period"]').val();

  var input_amount = $('input[name="amount"]').val();

  var level_label = $('.level');

  if (frequency == 'monthly') {
    // detemine level and update text based on monthly frequency
    if (input_amount > 3 && input_amount <= 5) {
      level_label.text('Enthusiast');
    } else if (input_amount > 5 && input_amount <= 12) {
      level_label.text('Activist');
    } else if (input_amount > 12 && input_amount <= 21) {
      level_label.text('Advocate');
    } else if (input_amount > 21 && input_amount <= 42) {
      level_label.text('Diplomat');
    } else if (input_amount > 42 && input_amount <= 83) {
      level_label.text('Benefactor');
    } else if (input_amount > 83 && input_amount <= 208) {
      level_label.text("Editor's Circle - $3,000 pledge");
    } else if (input_amount > 208 && input_amount <= 416) {
      level_label.text('Leadership Circle - $7,500 pledge');
    } else if (input_amount > 416) {
      level_label.text("Chairman's Circle - $15,000 pledge");
    }
  } else {
    // detemine level and update text based on yearly frequency
    if (input_amount == 10) {
      level_label.text('Student');
    } else if (input_amount > 35 && input_amount <= 59) {
      level_label.text('Enthusiast');
    } else if (input_amount > 59 && input_amount <= 149) {
      level_label.text('Activist');
    } else if (input_amount > 149 && input_amount <= 249) {
      level_label.text('Advocate');
    } else if (input_amount > 249 && input_amount <= 499) {
      level_label.text('Diplomat');
    } else if (input_amount > 499 && input_amount <= 999) {
      level_label.text('Benefactor');
    } else if (input_amount > 999 && input_amount <= 2499) {
      level_label.text("Editor's Circle - $3,000 pledge");
    } else if (input_amount > 2499 && input_amount <= 4999) {
      level_label.text('Leadership Circle - $7,500 pledge');
    } else if (input_amount > 4999) {
      level_label.text("Chairman's Circle - $15,000 pledge");
    }
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

  // When status is open, installments is always None
  openended_status_open.click(function() {
    installments.val("None");
  });

  // when status is none for yearly members, installments should be 1
  openended_status_none.click(function() {
    installments.val("1");
  });
};

var pay_fee_amount = function() {
  var input_amount = $('input[name="amount"]').val();
  var pay_fee_element = $('#pay-fee-amount span');

  // Calculate the Stripe fee per charge
  // https://stripe.com/us/pricing
  input_amount *= 0.029;
  input_amount += 0.30;

  input_amount = Math.round(input_amount * 100) / 100;

  // Make sure to always get two decimal places
  input_amount = input_amount.toFixed(2);

  // Add a dollar sign
  pay_fee_element.text('$' + input_amount);
};
