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

export const isZip = value => {
  return this.isNumeric(value) && value.trim().length === 5;
};

export const isNotEmpty = value => {
  return !validate.isEmpty(value.trim());
};

export const isEmptyOrZip = value => {
  if (!this.isNotEmpty(value)) return true;
  return this.isZip(value);
};

export const isValidDonationAmount = value => {
  const isValid = validate(
    { value: value.trim() },
    { value: { numericality: { greaterThanOrEqualTo: 1 } } }
  );
  return typeof isValid === 'undefined';
};

export const isMaxLength = maxLength => {
  return value => value.trim().length <= maxLength;
};

export const isNotEmptyAndIsMaxLength = maxLength => {
  return value => this.isNotEmpty(value) && value.trim().length <= maxLength;
};

export const isURL = value => {
  const isValid = validate(
    { website: value.trim() },
    { website: { url: true } }
  );
  return typeof isValid === 'undefined';
};

export const isValidWebsite = value => {
  return this.isURL(value) && this.isMaxLength(255)(value);
};
