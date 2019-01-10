import * as validators from '../../utils/validators';

export const CIRCLE_BUCKETS = {
  editorMonthly: {
    bucket: 'editor',
    installmentPeriod: 'monthly',
    amount: '84',
    installments: '36',
  },
  editorYearly: {
    bucket: 'editor',
    installmentPeriod: 'yearly',
    amount: '1000',
    installments: '3',
  },
  leadershipMonthly: {
    bucket: 'leadership',
    installmentPeriod: 'monthly',
    amount: '209',
    installments: '36',
  },
  leadershipYearly: {
    bucket: 'leadership',
    installmentPeriod: 'yearly',
    amount: '2500',
    installments: '3',
  },
  chairmanMonthly: {
    bucket: 'chairman',
    installmentPeriod: 'monthly',
    amount: '417',
    installments: '36',
  },
  chairmanYearly: {
    bucket: 'chairman',
    installmentPeriod: 'yearly',
    amount: '5000',
    installments: '3',
  },
};

export const CIRCLE_FORM_STATE = {
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
    validator: validators.isEmptyOrZip,
    message: 'Enter a 5-digit zip code',
  },
  pay_fees_value: {
    value: 'False',
    isValid: true,
    validator: null,
    message: null,
  },
  description: {
    value: 'The Texas Tribune Circle Membership',
    isValid: true,
    validator: null,
    message: null,
  },
  openended_status: {
    value: 'None',
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
  level: { value: '', isValid: true, validator: null, message: null },
  campaign_id: { value: '', isValid: true, validator: null, message: null },
  referral_id: { value: '', isValid: true, validator: null, message: null },
  amount: { value: '', isValid: true, validator: null, message: null },
  installments: { value: '', isValid: true, validator: null, message: null },
};
