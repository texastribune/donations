import * as validators from '../../utils/validators';

const LONG_PROGRAM_NAME = 'The Texas Tribune Business Membership';
const DEFAULT_PAY_FEES = 'True';
const DEFAULT_STATE_SELECTED = 'TX';

// master setting for default selection
export const DEFAULT_LEVEL = 'bigTexYearly';

// no order dependency in code for these.
// the key is the bucket
export const BUSINESS_LEVELS = {
  bigTexYearly: {
    bucket: 'bigTex',
    bucketFull: 'Big Tex',
    installmentPeriod: 'yearly',
    amount: '2500',
  },
  bigTexMonthly: {
    bucket: 'bigTex',
    bucketFull: 'Big Tex',
    installmentPeriod: 'monthly',
    amount: '208',
  },
  loneStarYearly: {
    bucket: 'loneStar',
    bucketFull: 'Lone Star',
    installmentPeriod: 'yearly',
    amount: '1500',
  },
  loneStarMonthly: {
    bucket: 'loneStar',
    bucketFull: 'Lone Star',
    installmentPeriod: 'monthly',
    amount: '125',
  },
  hatsOffYearly: {
    bucket: 'hatsOff',
    bucketFull: "Hat's Off",
    installmentPeriod: 'yearly',
    amount: '500',
  },
  hatsOffMonthly: {
    bucket: 'hatsOff',
    bucketFull: "Hat's Off",
    installmentPeriod: 'monthly',
    amount: '42',
  },
};

// for select list
export const US_STATES_SELECT_LIST = [
  { id: 0, value: 'AL', text: 'Alabama' },
  { id: 1, value: 'AK', text: 'Alaska' },
  { id: 2, value: 'AZ', text: 'Arizona' },
  { id: 3, value: 'AR', text: 'Arkansas' },
  { id: 4, value: 'CA', text: 'California' },
  { id: 5, value: 'CO', text: 'Colorado' },
  { id: 6, value: 'CT', text: 'Connecticut' },
  { id: 7, value: 'DE', text: 'Delaware' },
  { id: 8, value: 'DC', text: 'District of Columbia' },
  { id: 9, value: 'FL', text: 'Florida' },
  { id: 10, value: 'GA', text: 'Georgia' },
  { id: 11, value: 'HI', text: 'Hawaii' },
  { id: 12, value: 'ID', text: 'Idaho' },
  { id: 13, value: 'IL', text: 'Illinois' },
  { id: 14, value: 'IN', text: 'Indiana' },
  { id: 15, value: 'IA', text: 'Iowa' },
  { id: 16, value: 'KS', text: 'Kansas' },
  { id: 17, value: 'KY', text: 'Kentucky' },
  { id: 18, value: 'LA', text: 'Louisiana' },
  { id: 19, value: 'ME', text: 'Maine' },
  { id: 20, value: 'MD', text: 'Maryland' },
  { id: 21, value: 'MA', text: 'Massachusetts' },
  { id: 22, value: 'MI', text: 'Michigan' },
  { id: 23, value: 'MN', text: 'Minnesota' },
  { id: 24, value: 'MS', text: 'Mississippi' },
  { id: 25, value: 'MO', text: 'Missouri' },
  { id: 26, value: 'MT', text: 'Montana' },
  { id: 27, value: 'NE', text: 'Nebraska' },
  { id: 28, value: 'NV', text: 'Nevada' },
  { id: 29, value: 'NH', text: 'New Hampshire' },
  { id: 30, value: 'NJ', text: 'New Jersey' },
  { id: 31, value: 'NM', text: 'New Mexico' },
  { id: 32, value: 'NY', text: 'New York' },
  { id: 33, value: 'NC', text: 'North Carolina' },
  { id: 34, value: 'ND', text: 'North Dakota' },
  { id: 35, value: 'OH', text: 'Ohio' },
  { id: 36, value: 'OK', text: 'Oklahoma' },
  { id: 37, value: 'OR', text: 'Oregon' },
  { id: 38, value: 'PA', text: 'Pennsylvania' },
  { id: 39, value: 'RI', text: 'Rhode Island' },
  { id: 40, value: 'SC', text: 'South Carolina' },
  { id: 41, value: 'SD', text: 'South Dakota' },
  { id: 42, value: 'TN', text: 'Tennessee' },
  { id: 43, value: 'TX', text: 'Texas' },
  { id: 44, value: 'UT', text: 'Utah' },
  { id: 45, value: 'VT', text: 'Vermont' },
  { id: 46, value: 'VA', text: 'Virginia' },
  { id: 47, value: 'WA', text: 'Washington' },
  { id: 48, value: 'WV', text: 'West Virginia' },
  { id: 49, value: 'WI', text: 'Wisconsin' },
  { id: 50, value: 'WY', text: 'Wyoming' },
];

export const BUSINESS_FORM_STATE = {
  stripeEmail: {
    value: '',
    isValid: false,
    validator: validators.isEmail,
    message: 'Enter a valid email address',
  },
  business_name: {
    value: '',
    isValid: false,
    validator: validators.isNotEmptyAndIsMaxLength(255),
    message: 'Enter a business name (255 characters or fewer)',
  },
  first_name: {
    value: '',
    isValid: false,
    validator: validators.isNotEmpty,
    message: 'Enter contact first name',
  },
  last_name: {
    value: '',
    isValid: false,
    validator: validators.isNotEmpty,
    message: 'Enter contact last name',
  },
  website: {
    value: '',
    isValid: false,
    validator: validators.isValidWebsite,
    message: 'Enter a website, including https:// or http://',
  },
  reason: {
    value: '',
    isValid: false,
    validator: validators.isMaxLength(255),
    message: 'Must be 255 characters or fewer',
  },
  shipping_postalcode: {
    value: '',
    isValid: false,
    validator: validators.isZip,
    message: 'Enter a 5-digit zip code',
  },
  shipping_street: {
    value: '',
    isValid: false,
    validator: validators.isNotEmptyAndIsMaxLength(255),
    message: 'Enter a street/mailing address (255 characters or fewer)',
  },
  shipping_city: {
    value: '',
    isValid: false,
    validator: validators.isNotEmptyAndIsMaxLength(40),
    message: 'Enter a city (40 characters or fewer)',
  },
  shipping_state: {
    value: DEFAULT_STATE_SELECTED,
    isValid: true,
    validator: null,
    message: null,
  },
  pay_fees_value: {
    value: DEFAULT_PAY_FEES,
    isValid: true,
    validator: null,
    message: null,
  },
  description: {
    value: LONG_PROGRAM_NAME,
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
  level: {
    value: '',
    isValid: true,
    validator: null,
    message: null,
  },
  campaign_id: {
    value: '',
    isValid: true,
    validator: null,
    message: null,
  },
  referral_id: {
    value: '',
    isValid: true,
    validator: null,
    message: null,
  },
  amount: {
    value: '',
    isValid: true,
    validator: null,
    message: null,
  },
};
