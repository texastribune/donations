import * as validators from '../../utils/validators';

export const DEFAULT_LEVEL = 'blastMonthly';

export const BLAST_LEVELS = {
  blastMonthly: {
    bucket: 'standard',
    bucketFull: 'Standard subscription',
    installmentPeriod: 'monthly',
    amount: '40',
    isDefault: true,
    footer: 'Save 27% with yearly',
  },
  blastYearly: {
    bucket: 'standard',
    bucketFull: 'Standard subscription',
    installmentPeriod: 'yearly',
    amount: '349',
  },
  blastTaxExempt: {
    bucket: 'tax-exempt',
    bucketFull: 'Tax-exempt subscription',
    installmentPeriod: 'yearly',
    amount: '325',
  },
  // blastAcademicMonthly: {
  //   bucket: 'academic',
  //   bucketFull: 'Academic discount',
  //   installmentPeriod: 'monthly',
  //   amount: '20',
  // },
  // blastAcademicYearly: {
  //   bucket: 'academic',
  //   bucketFull: 'Academic discount',
  //   installmentPeriod: 'yearly',
  //   amount: '199',
  // },
  // blastLegislativeSession: {
  //   bucket: 'legislative',
  //   bucketFull: 'Legislative session-only',
  //   installmentPeriod: 'one-time',
  //   amount: '200',
  //   isFeatured: true,
  //   prompt: 'Get ahead with insider news!',
  //   footer: 'January 14 – June 14',
  // },
  blastSpecialSession: {
    bucket: 'special',
    bucketFull: 'Special session pricing',
    installmentPeriod: 'one-time for 2025',
    amount: '100',
    isFeatured: true,
    prompt: 'Get ahead with insider news!',
    footer: 'Renews at $250 in 2026',
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
  pay_fees_value: {
    value: 'False',
    isValid: true,
    validator: null,
    message: null,
  },
  description: {
    value: 'The Blast Subscription',
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
