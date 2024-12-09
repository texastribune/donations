import * as validators from '../../utils/validators';

export const DEFAULT_LEVEL = 'blastMonthly';

export const BLAST_LEVELS = {
  blastMonthly: {
    bucket: 'standard',
    bucketFull: 'Standard subscription',
    installmentPeriod: 'monthly',
    amount: '40',
  },
  blastYearly: {
    bucket: 'standard',
    bucketFull: 'Standard subscription',
    installmentPeriod: 'yearly',
    amount: '349',
  },
  blastTaxExemptYearly: {
    bucket: 'tax-exempt',
    bucketFull: 'Tax-exempt subscription',
    installmentPeriod: 'yearly',
    amount: '325',
  },
  blastAcademicMonthly: {
    bucket: 'academic',
    bucketFull: 'Academic discount',
    installmentPeriod: 'monthly',
    amount: '20',
  },
  blastAcademicYearly: {
    bucket: 'academic',
    bucketFull: 'Academic discount',
    installmentPeriod: 'yearly',
    amount: '199',
  },
  blastLegislativeYearly: {
    bucket: 'legislative',
    bucketFull: 'Legislative session-only',
    installmentPeriod: 'yearly',
    amount: '240',
  },
};

export const BLAST_FORM_STATE = {
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
