import * as validators from '../../utils/validators';

export const AMBASSADOR_CODES = {
  'ump-1': {
    installmentPeriod: 'monthly',
    amount: '15',
  },
};

export const BASE_FORM_STATE = {
  stripeEmail: {
    value: '',
    isValid: false,
    validator: validators.isEmail,
    message: 'Enter a valid email address',
  },
  first_name: {
    value: '',
    isValid: false,
    validator: validators.isNotEmpty,
    message: 'Enter your first name',
  },
  last_name: {
    value: '',
    isValid: false,
    validator: validators.isNotEmpty,
    message: 'Enter your last name',
  },
  reason: {
    value: '',
    isValid: false,
    validator: validators.isMaxLength(255),
    message: 'Must be 255 characters or fewer',
  },
  zipcode: {
    value: '',
    isValid: false,
    validator: validators.isZip,
    message: 'Enter a 5-digit zip code',
  },
  amount: {
    value: '',
    isValid: false,
    validator: validators.isValidDonationAmount,
    message: 'Enter numeric amount above $1',
  },
  pay_fees_value: {
    value: 'False',
    isValid: true,
    validator: null,
    message: null,
  },
  description: {
    value: 'The Texas Tribune Membership',
    isValid: true,
    validator: null,
    message: null,
  },
  installment_period: {
    value: '',
    isValid: true,
    validator: null,
    message: null,
  },
  campaign_id: { value: '', isValid: true, validator: null, message: null },
  referral_id: { value: '', isValid: true, validator: null, message: null },
  // proof tells us if we should engage changes we are ab testing
  proof: { value: false, isValid: true, validator: null, message: null },
};
