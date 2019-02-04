import * as validators from '../../utils/validators';

export const POSITION_ON_FORM_0 = 0;
export const POSITION_ON_FORM_1 = 1;
export const POSITION_ON_FORM_2 = 2;
export const LONG_PROGRAM_NAME = 'The Texas Tribune Business Membership';

// to reorder the buckets (donation levels) on the page, reorder this array
// the logic automatically follows
export const MEMBERSHIP_LEVELS = [
  { header: 'Big Tex', amount: 2500 },
  { header: 'Lone Star', amount: 1500 },
  { header: "Hat's Off!", amount: 500 },
];

// query related
export const QUERY_PARAMETERS_STRING_VALUES = {
  oneStr: '1',
  onceStr: 'once',
  oneTimeStr: 'one-time',
  openStr: 'Open',
  noneStr: 'None',
  monthlyStr: 'monthly',
  yearlyStr: 'yearly',
  annuallyStr: 'annually',
};

// back-end form to UI translations for the different payment options (common radio buttons)
const MONTHLY_PAYMENTS = {
  installmentPeriod: QUERY_PARAMETERS_STRING_VALUES.monthlyStr,
  installmentsPerYear: 12,
  installments: QUERY_PARAMETERS_STRING_VALUES.noneStr,
  openEndedStatus: QUERY_PARAMETERS_STRING_VALUES.openStr,
  uiInstallmentPeriod: QUERY_PARAMETERS_STRING_VALUES.monthlyStr,
};
const YEARLY_PAYMENT = {
  installmentPeriod: QUERY_PARAMETERS_STRING_VALUES.yearlyStr,
  installmentsPerYear: 1,
  installments: QUERY_PARAMETERS_STRING_VALUES.noneStr,
  openEndedStatus: QUERY_PARAMETERS_STRING_VALUES.openStr,
  uiInstallmentPeriod: QUERY_PARAMETERS_STRING_VALUES.annuallyStr,
};

// common structure and var names used by the donation apps
// plugs into the common donate app code
export const DEFAULT_PAY_FEES = 'True';

// no order dependency in code for these.
// the key is the bucket
export const BUSINESS_BUCKETS = {
  levelAMonthly: {
    bucket: 'levelA',
    amount: Math.round(
      MEMBERSHIP_LEVELS[POSITION_ON_FORM_0].amount /
        MONTHLY_PAYMENTS.installmentsPerYear
    ).toString(),
    paymentDetails: MONTHLY_PAYMENTS,
    payFees: DEFAULT_PAY_FEES,
  },
  levelAYearly: {
    bucket: 'levelA',
    amount: (
      MEMBERSHIP_LEVELS[POSITION_ON_FORM_0].amount /
      YEARLY_PAYMENT.installmentsPerYear
    ).toString(),
    paymentDetails: YEARLY_PAYMENT,
    payFees: DEFAULT_PAY_FEES,
  },
  levelBMonthly: {
    bucket: 'levelB',
    amount: Math.round(
      MEMBERSHIP_LEVELS[POSITION_ON_FORM_1].amount /
        MONTHLY_PAYMENTS.installmentsPerYear
    ).toString(),
    paymentDetails: MONTHLY_PAYMENTS,
    payFees: DEFAULT_PAY_FEES,
  },
  levelBYearly: {
    bucket: 'levelB',
    amount: (
      MEMBERSHIP_LEVELS[POSITION_ON_FORM_1].amount /
      YEARLY_PAYMENT.installmentsPerYear
    ).toString(),
    paymentDetails: YEARLY_PAYMENT,
    payFees: DEFAULT_PAY_FEES,
  },
  levelCMonthly: {
    bucket: 'levelC',
    amount: Math.round(
      MEMBERSHIP_LEVELS[POSITION_ON_FORM_2].amount /
        MONTHLY_PAYMENTS.installmentsPerYear
    ).toString(),
    paymentDetails: MONTHLY_PAYMENTS,
    payFees: DEFAULT_PAY_FEES,
  },
  levelCYearly: {
    bucket: 'levelC',
    amount: (
      MEMBERSHIP_LEVELS[POSITION_ON_FORM_2].amount /
      YEARLY_PAYMENT.installmentsPerYear
    ).toString(),
    paymentDetails: YEARLY_PAYMENT,
    payFees: DEFAULT_PAY_FEES,
  },
};

// master setting for default selection
export const DEFAULT_DONATION_LEVEL_WITH_INSTALL_PERIOD = 'levelAYearly';
export const DEFAULT_ONCE_DONATION_LEVEL_WITH_INSTALL_PERIOD = 'levelAOneTime';

// Texas will be default selection on state list
export const DEFAULT_STATE_SELECTED = 'TX'; // Texas

// whitelisting and query params
// add new query parameters here to whitelist them
export const WL_DEFAULT_PARAMETERS = {
  campaignId: '',
  referralId: '',
  installments:
    BUSINESS_BUCKETS[DEFAULT_DONATION_LEVEL_WITH_INSTALL_PERIOD].paymentDetails
      .installments,
  installmentPeriod:
    BUSINESS_BUCKETS[DEFAULT_DONATION_LEVEL_WITH_INSTALL_PERIOD].paymentDetails
      .installmentPeriod,
  // special processing for these
  // (looks redundant but this is per backend and requestor requirements
  installment_period:
    BUSINESS_BUCKETS[DEFAULT_DONATION_LEVEL_WITH_INSTALL_PERIOD].paymentDetails
      .installmentPeriod,
  openended_status:
    BUSINESS_BUCKETS[DEFAULT_DONATION_LEVEL_WITH_INSTALL_PERIOD].paymentDetails
      .openEndedStatus,
};

// guard against processing insanely long query strings from spec
export const WL_QUERY_PARAMETERS_MAX_NBR_CHARS = 18;
export const WL_QUERY_ESCAPE_THRESHOLD = 6;

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
  openended_status: {
    value: '',
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
