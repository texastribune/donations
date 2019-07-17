import * as validators from '../../utils/validators';

export const DEFAULT_LEVEL = 'editorMonthly';

export const CIRCLE_LEVELS = {
  editorMonthly: {
    bucket: 'editor',
    bucketFull: "Editor's Circle",
    installmentPeriod: 'monthly',
    amount: '84',
  },
  editorYearly: {
    bucket: 'editor',
    bucketFull: "Editor's Circle",
    installmentPeriod: 'yearly',
    amount: '1000',
  },
  leadershipMonthly: {
    bucket: 'leadership',
    bucketFull: 'Leadership Circle',
    installmentPeriod: 'monthly',
    amount: '209',
  },
  leadershipYearly: {
    bucket: 'leadership',
    bucketFull: 'Leadership Circle',
    installmentPeriod: 'yearly',
    amount: '2500',
  },
  chairmanMonthly: {
    bucket: 'chairman',
    bucketFull: "Chairman's Circle",
    installmentPeriod: 'monthly',
    amount: '417',
  },
  chairmanYearly: {
    bucket: 'chairman',
    bucketFull: "Chairman's Circle",
    installmentPeriod: 'yearly',
    amount: '5000',
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
};
