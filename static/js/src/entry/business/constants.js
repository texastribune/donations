// eslint-disable-POSITION_ON_FORM_0next-line import/prefer-default-export
export const POSITION_ON_FORM_0 = 0;
export const POSITION_ON_FORM_1 = 1;
export const POSITION_ON_FORM_2 = 2;
export const LONG_PROGRAM_NAME = 'The Texas Tribune Business Membership';

const MEMBERSHIP_LEVELS_COMMON_SUBHEADER = ' donation';
export const MEMBERSHIP_LEVELS = [
  { header: 'Hat\'s Off!', amount: 500, subheader: MEMBERSHIP_LEVELS_COMMON_SUBHEADER }, // A
  { header: 'Lone Star', amount: 1500, subheader: MEMBERSHIP_LEVELS_COMMON_SUBHEADER }, // B
  { header: 'Big Tex', amount: 2500, subheader: MEMBERSHIP_LEVELS_COMMON_SUBHEADER }, // C
];

//
// Query related
//
export const QUERY_PARAMETERS_STRING_VALUES = {
  oneStr: '1',
  onceStr: 'once',
  openStr: 'Open',
  noneStr: 'None',
  monthlyStr: 'monthly',
  yearlyStr: 'yearly',
};

//
//
// Back-end form to UI translations for the different payment options (common radio buttons)
//
const MONTHLY_PAYMENTS = {
  installmentPeriod: QUERY_PARAMETERS_STRING_VALUES.monthlyStr,
  installmentsPerYear: 12,
  installments: QUERY_PARAMETERS_STRING_VALUES.noneStr,
  openEndedStatus: QUERY_PARAMETERS_STRING_VALUES.openStr,
};
const YEARLY_PAYMENT = {
  installmentPeriod: QUERY_PARAMETERS_STRING_VALUES.yearlyStr,
  installmentsPerYear: 1,
  installments: QUERY_PARAMETERS_STRING_VALUES.noneStr,
  openEndedStatus: QUERY_PARAMETERS_STRING_VALUES.openStr,
};
const ONETIME_PAYMENT = {
  installmentPeriod: QUERY_PARAMETERS_STRING_VALUES.onceStr,
  installmentsPerYear: 1,
  installments: QUERY_PARAMETERS_STRING_VALUES.oneStr,
  openEndedStatus: QUERY_PARAMETERS_STRING_VALUES.noneStr,
};

//
// Common structure and var names used by the family of SF-S apps
// Plugs into the common donate app code
//
const DEFAULT_PAY_FEES = 'True';

export const BUSINESS_BUCKETS = {
  levelAMonthly: {
    bucket: 'levelA',
    amount: Math.round(MEMBERSHIP_LEVELS[POSITION_ON_FORM_0].amount / MONTHLY_PAYMENTS.installmentsPerYear).toString(),
    paymentDetails: MONTHLY_PAYMENTS,
    payFees: DEFAULT_PAY_FEES,
  },
  levelAYearly: {
    bucket: 'levelA',
    amount: (MEMBERSHIP_LEVELS[POSITION_ON_FORM_0].amount / YEARLY_PAYMENT.installmentsPerYear).toString(),
    paymentDetails: YEARLY_PAYMENT,
    payFees: DEFAULT_PAY_FEES,
  },
  levelAOneTime: {
    bucket: 'levelA',
    amount: (MEMBERSHIP_LEVELS[POSITION_ON_FORM_0].amount / ONETIME_PAYMENT.installmentsPerYear).toString(),
    paymentDetails: ONETIME_PAYMENT,
    payFees: DEFAULT_PAY_FEES,
  },
  levelBMonthly: {
    bucket: 'levelB',
    amount: Math.round(MEMBERSHIP_LEVELS[POSITION_ON_FORM_1].amount / MONTHLY_PAYMENTS.installmentsPerYear).toString(),
    paymentDetails: MONTHLY_PAYMENTS,
    payFees: DEFAULT_PAY_FEES,
  },
  levelBYearly: {
    bucket: 'levelB',
    amount: (MEMBERSHIP_LEVELS[POSITION_ON_FORM_1].amount / YEARLY_PAYMENT.installmentsPerYear).toString(),
    paymentDetails: YEARLY_PAYMENT,
    payFees: DEFAULT_PAY_FEES,
  },
  levelBOneTime: {
    bucket: 'levelB',
    amount: (MEMBERSHIP_LEVELS[POSITION_ON_FORM_1].amount / ONETIME_PAYMENT.installmentsPerYear).toString(),
    paymentDetails: ONETIME_PAYMENT,
    payFees: DEFAULT_PAY_FEES,
  },
  levelCMonthly: {
    bucket: 'levelC',
    amount: Math.round(MEMBERSHIP_LEVELS[POSITION_ON_FORM_2].amount / MONTHLY_PAYMENTS.installmentsPerYear).toString(),
    paymentDetails: MONTHLY_PAYMENTS,
    payFees: DEFAULT_PAY_FEES,
  },
  levelCYearly: {
    bucket: 'levelC',
    amount: (MEMBERSHIP_LEVELS[POSITION_ON_FORM_2].amount / YEARLY_PAYMENT.installmentsPerYear).toString(),
    paymentDetails: YEARLY_PAYMENT,
    payFees: DEFAULT_PAY_FEES,
  },
  levelCOneTime: {
    bucket: 'levelC',
    amount: (MEMBERSHIP_LEVELS[POSITION_ON_FORM_2].amount / ONETIME_PAYMENT.installmentsPerYear).toString(),
    paymentDetails: ONETIME_PAYMENT,
    payFees: DEFAULT_PAY_FEES,
  },
};

//
// MASTER Setting for default selection
//
export const DEFAULT_DONATION_LEVEL_WITH_INSTALL_PERIOD = 'levelAYearly';
export const DEFAULT_ONCE_DONATION_LEVEL_WITH_INSTALL_PERIOD = 'levelAOneTime';

//
// Texas will be default selection on state list
//
export const DEFAULT_STATE_SELECTED = 'TX'; // Texas

//
// Whitelisting and query params
// Add new query parameters here to whitelist them
//
export const WL_DEFAULT_QUERY_PARAMETERS = {
  campaignId: '',
  referralId: '',
  installments: BUSINESS_BUCKETS[DEFAULT_DONATION_LEVEL_WITH_INSTALL_PERIOD].paymentDetails.installments,
  installmentPeriod: BUSINESS_BUCKETS[DEFAULT_DONATION_LEVEL_WITH_INSTALL_PERIOD].paymentDetails.installmentPeriod,
  // Special processing for these
  // (looks redundant but this is per backend and requestor requirements
  installment_period: BUSINESS_BUCKETS[DEFAULT_DONATION_LEVEL_WITH_INSTALL_PERIOD].paymentDetails.installmentPeriod,
  openended_status: BUSINESS_BUCKETS[DEFAULT_DONATION_LEVEL_WITH_INSTALL_PERIOD].paymentDetails.openEndedStatus,
};

//
// Guard against processing insanely long query strings
//
export const WL_QUERY_PARAMETERS_MAX_NBR_CHARS = 18; // From spec
export const WL_QUERY_ESCAPE_THRESHOLD = 6;
