
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

var pay_fee_amount = function() {
  var input_amount = $('select[name="amount"]').val();
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
