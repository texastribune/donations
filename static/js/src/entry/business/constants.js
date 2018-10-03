// eslint-disable-next-line import/prefer-default-export
export const POSITION_0 = 0;
export const POSITION_1 = 1;
export const POSITION_2 = 2;
export const LONG_PROGRAM_NAME = 'The Texas Tribune Business Membership';
export const SHORT_PROGRAM_NAME = 'Business Membership';

export const MEMBERSHIP_LEVELS = [
  { header: 'Hat\'s Off!', amount: 500  },  // A
  { header: 'Lone Star',   amount: 1500 }, // B
  { header: 'Big Tex',     amount: 2500 }, // C
];

const DEFAULT_PAY_FEES = 'True';
const MONTHLY_PAYMENTS = { text:'monthly donation',  installmentsPerYear: 12, recurring: true };
const ONETIME_PAYMENT  = { text:'one-time donation', installmentsPerYear: 1,  recurring: false };
const YEARLY_PAYMENT   = { text:'yearly donation',   installmentsPerYear: 1,  recurring: true };

//
// Common structure and var names used by the family of SF-S apps
// Plugs into the common code
//
export const BUSINESS_BUCKETS = {
  levelAMonthly: {
    bucket: 'levelA',
    header: MEMBERSHIP_LEVELS[POSITION_0].header,
    amount: Math.trunc( MEMBERSHIP_LEVELS[POSITION_0].amount / MONTHLY_PAYMENTS.installmentsPerYear ),
    installmentPeriod: MONTHLY_PAYMENTS.text,
    installments: MONTHLY_PAYMENTS.installmentsPerYear,
    recurring: MONTHLY_PAYMENTS.recurring,
    payFees: DEFAULT_PAY_FEES,
  },
  levelAYearly: {
    bucket: 'levelA',
    header: MEMBERSHIP_LEVELS[POSITION_0].header,
    amount: MEMBERSHIP_LEVELS[POSITION_0].amount / YEARLY_PAYMENT.installmentsPerYear,
    installmentPeriod: YEARLY_PAYMENT.text,
    installments: MEMBERSHIP_LEVELS[POSITION_0].amount,
    recurring: YEARLY_PAYMENT.recurring,
    payFees: DEFAULT_PAY_FEES,
  },
  levelAOneTime: {
    bucket: 'levelA',
    header: MEMBERSHIP_LEVELS[POSITION_0].header,
    amount: MEMBERSHIP_LEVELS[POSITION_0].amount / ONETIME_PAYMENT.installmentsPerYear,
    installmentPeriod: ONETIME_PAYMENT.text,
    installments: MEMBERSHIP_LEVELS[POSITION_0].amount,
    recurring: ONETIME_PAYMENT.recurring,
    payFees: DEFAULT_PAY_FEES,
  },
  levelBMonthly: {
    bucket: 'levelB',
    header: MEMBERSHIP_LEVELS[POSITION_1].header,
    amount: Math.trunc(MEMBERSHIP_LEVELS[POSITION_1].amount / MONTHLY_PAYMENTS.installmentsPerYear),
    installmentPeriod: MONTHLY_PAYMENTS.text,
    installments: MONTHLY_PAYMENTS.installmentsPerYear,
    recurring: MONTHLY_PAYMENTS.recurring,
    payFees: DEFAULT_PAY_FEES,
  },
  levelBYearly: {
    bucket: 'levelB',
    header: MEMBERSHIP_LEVELS[POSITION_1].header,
    amount: MEMBERSHIP_LEVELS[POSITION_1].amount,
    installmentPeriod: YEARLY_PAYMENT.text,
    installments: YEARLY_PAYMENT.installmentsPerYear,
    payFees: DEFAULT_PAY_FEES,
  },
  levelBOneTime: {
    bucket: 'levelB',
    header: MEMBERSHIP_LEVELS[POSITION_1].header,
    amount: MEMBERSHIP_LEVELS[POSITION_1].amount / ONETIME_PAYMENT.installmentsPerYear,
    installmentPeriod: ONETIME_PAYMENT.text,
    installments: MEMBERSHIP_LEVELS[POSITION_0].amount,
    recurring: ONETIME_PAYMENT.recurring,
    payFees: DEFAULT_PAY_FEES,
  },
  levelCMonthly: {
    bucket: 'levelC',
    header: MEMBERSHIP_LEVELS[POSITION_2].header,
    amount: Math.trunc(MEMBERSHIP_LEVELS[POSITION_2].amount / MONTHLY_PAYMENTS.installmentsPerYear),
    installmentPeriod: MONTHLY_PAYMENTS.text,
    installments: MONTHLY_PAYMENTS.installmentsPerYear,
    recurring: MONTHLY_PAYMENTS.recurring,
    payFees: DEFAULT_PAY_FEES,
  },
  levelCYearly: {
    bucket: 'levelC',
    header: MEMBERSHIP_LEVELS[POSITION_2].header,
    amount: MEMBERSHIP_LEVELS[POSITION_2].amount,
    installmentPeriod: YEARLY_PAYMENT.text,
    installments: YEARLY_PAYMENT.installmentsPerYear,
    payFees: DEFAULT_PAY_FEES,
  },
  levelCOneTime: {
    bucket: 'levelC',
    header: MEMBERSHIP_LEVELS[POSITION_2].header,
    amount: MEMBERSHIP_LEVELS[POSITION_2].amount / ONETIME_PAYMENT.installmentsPerYear,
    installmentPeriod: ONETIME_PAYMENT.text,
    installments: MEMBERSHIP_LEVELS[POSITION_0].amount,
    recurring: ONETIME_PAYMENT.recurring,
    payFees: DEFAULT_PAY_FEES,
  },
};

//
// Set defaults in this file where everything else is initialized
//
export const DEFAULT_SELECT_BUCKET = BUSINESS_BUCKETS[POSITION_0];
export const DEFAULT_SELECTOR_LEVEL = 'levelAMonthly';

//
// Generic data format for using the SelectList Vue component
// US States and territories for select state list
// Using the DOM standard naming convention for select data fields
//
export const DEFAULT_STATE_SELECTED = 43; // Texas
export const US_STATES_SELECT_LIST = [
  { value: 'AL', text: 'Alabama' },
  { value: 'AK', text: 'Alaska' },
  { value: 'AZ', text: 'Arizona' },
  { value: 'AR', text: 'Arkansas' },
  { value: 'CA', text: 'California' },
  { value: 'CO', text: 'Colorado' },
  { value: 'CT', text: 'Connecticut' },
  { value: 'DE', text: 'Delaware' },
  { value: 'DC', text: 'District of Columbia' },
  { value: 'FL', text: 'Florida' },
  { value: 'GA', text: 'Georgia' },
  { value: 'HI', text: 'Hawaii' },
  { value: 'ID', text: 'Idaho' },
  { value: 'IL', text: 'Illinois' },
  { value: 'IN', text: 'Indiana' },
  { value: 'IA', text: 'Iowa' },
  { value: 'KS', text: 'Kansas' },
  { value: 'KY', text: 'Kentucky' },
  { value: 'LA', text: 'Louisiana' },
  { value: 'ME', text: 'Maine' },
  { value: 'MD', text: 'Maryland' },
  { value: 'MA', text: 'Massachusetts' },
  { value: 'MI', text: 'Michigan' },
  { value: 'MN', text: 'Minnesota' },
  { value: 'MS', text: 'Mississippi' },
  { value: 'MO', text: 'Missouri' },
  { value: 'MT', text: 'Montana' },
  { value: 'NE', text: 'Nebraska' },
  { value: 'NV', text: 'Nevada' },
  { value: 'NH', text: 'New Hampshire' },
  { value: 'NJ', text: 'New Jersey' },
  { value: 'NM', text: 'New Mexico' },
  { value: 'NY', text: 'New York' },
  { value: 'NC', text: 'North Carolina' },
  { value: 'ND', text: 'North Dakota' },
  { value: 'OH', text: 'Ohio' },
  { value: 'OK', text: 'Oklahoma' },
  { value: 'OR', text: 'Oregon' },
  { value: 'PA', text: 'Pennsylvania' },
  { value: 'RI', text: 'Rhode Island' },
  { value: 'SC', text: 'South Carolina' },
  { value: 'SD', text: 'South Dakota' },
  { value: 'TN', text: 'Tennessee' },
  { value: 'TX', text: 'Texas' },
  { value: 'UT', text: 'Utah' },
  { value: 'VT', text: 'Vermont' },
  { value: 'VA', text: 'Virginia' },
  { value: 'WA', text: 'Washington' },
  { value: 'WV', text: 'West Virginia' },
  { value: 'WI', text: 'Wisconsin' },
  { value: 'WY', text: 'Wyoming' },
];
