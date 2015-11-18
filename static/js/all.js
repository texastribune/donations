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
      level_label.text("Editor's Circle");
    } else if (input_amount > 208 && input_amount <= 416) {
      level_label.text('Leadership Circle');
    } else if (input_amount > 416) {
      level_label.text("Chairman's Circle");
    }
  } else {
    // detemine level and update text based on yearly frequency
    if (input_amount > 35 && input_amount <= 59) {
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
      level_label.text("Editor's Circle");
    } else if (input_amount > 2499 && input_amount <= 4999) {
      level_label.text('Leadership Circle');
    } else if (input_amount > 4999) {
      level_label.text("Chairman's Circle");
    }
  }
}
