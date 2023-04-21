import validate from 'validate.js';

export const isEmail = value => {
  const isValid = validate({ email: value.trim() }, { email: { email: true } });
  return typeof isValid === 'undefined';
};

export const isNumeric = value => {
  const isValid = validate(
    { value: value.trim() },
    { value: { numericality: true } }
  );
  return typeof isValid === 'undefined';
};

export const isZip = value => isNumeric(value) && value.trim().length === 5;

export const isNotEmpty = value => !validate.isEmpty(value.trim());

export const isEmptyOrZip = value => {
  if (!isNotEmpty(value)) return true;
  return isZip(value);
};

export const isValidDonationAmount = value => {
  let valueToCheck;

  if (value.charAt(0) === '$') {
    valueToCheck = value.substring(1);
  } else {
    valueToCheck = value;
  }

  const isValid = validate(
    { value: valueToCheck.trim() },
    { value: { numericality: { greaterThanOrEqualTo: 1 } } }
  );
  return typeof isValid === 'undefined';
};

export const isMaxLength = maxLength => value =>
  value.trim().length <= maxLength;

export const isNotEmptyAndIsMaxLength = maxLength => value =>
  isNotEmpty(value) && value.trim().length <= maxLength;

export const isURL = value => {
  const isValid = validate(
    { website: value.trim() },
    { website: { url: true } }
  );
  return typeof isValid === 'undefined';
};

export const isValidWebsite = value => isURL(value) && isMaxLength(255)(value);
