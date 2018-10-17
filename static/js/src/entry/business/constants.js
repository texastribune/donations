// eslint-disable-POSITION_ON_FORM_0next-line import/prefer-default-export
export const POSITION_ON_FORM_0 = 0;
export const POSITION_ON_FORM_1 = 1;
export const POSITION_ON_FORM_2 = 2;
export const LONG_PROGRAM_NAME = 'The Texas Tribune Business Membership';
export const SHORT_PROGRAM_NAME = 'Business Membership';

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
  text: 'monthly',
  installmentsPerYear: 12,
  formInstallmentsValue: QUERY_PARAMETERS_STRING_VALUES.noneStr,
  formOpenEndedStatus: QUERY_PARAMETERS_STRING_VALUES.openStr,
};
const YEARLY_PAYMENT = {
  text: 'yearly',
  installmentsPerYear: 1,
  formInstallmentsValue: QUERY_PARAMETERS_STRING_VALUES.noneStr,
  formOpenEndedStatus: QUERY_PARAMETERS_STRING_VALUES.openStr,
};
const ONETIME_PAYMENT = {
  text: 'one-time',
  installmentsPerYear: 1,
  formInstallmentsValue: QUERY_PARAMETERS_STRING_VALUES.oneStr,
  formOpenEndedStatus: QUERY_PARAMETERS_STRING_VALUES.noneStr,
};
//
// Common structure and var names used by the family of SF-S apps
// Plugs into the common code
// --[ REFACTOR candidate: Use payment details object defined above directly ]--
//
const DEFAULT_PAY_FEES = 'True';

export const BUSINESS_BUCKETS = {
  levelAMonthly: {
    bucket: 'levelA',
    amount: Math.round(MEMBERSHIP_LEVELS[POSITION_ON_FORM_0].amount / MONTHLY_PAYMENTS.installmentsPerYear).toString(),
    // paymentDetails: MONTHLY_PAYMENTS
    installments: MONTHLY_PAYMENTS.formInstallmentsValue,
    installmentPeriod: MONTHLY_PAYMENTS.text,
    openEndedStatus: MONTHLY_PAYMENTS.formOpenEndedStatus,
    payFees: DEFAULT_PAY_FEES,
  },
  levelAYearly: {
    bucket: 'levelA',
    amount: (MEMBERSHIP_LEVELS[POSITION_ON_FORM_0].amount / YEARLY_PAYMENT.installmentsPerYear).toString(),
    installments: YEARLY_PAYMENT.formInstallmentsValue,
    installmentPeriod: YEARLY_PAYMENT.text,
    openEndedStatus: YEARLY_PAYMENT.formOpenEndedStatus,
    payFees: DEFAULT_PAY_FEES,
  },
  levelAOneTime: {
    bucket: 'levelA',
    amount: (MEMBERSHIP_LEVELS[POSITION_ON_FORM_0].amount / ONETIME_PAYMENT.installmentsPerYear).toString(),
    installments: ONETIME_PAYMENT.formInstallmentsValue,
    installmentPeriod: ONETIME_PAYMENT.text,
    openEndedStatus: ONETIME_PAYMENT.formOpenEndedStatus,
    payFees: DEFAULT_PAY_FEES,
  },
  levelBMonthly: {
    bucket: 'levelB',
    amount: Math.round(MEMBERSHIP_LEVELS[POSITION_ON_FORM_1].amount / MONTHLY_PAYMENTS.installmentsPerYear).toString(),
    installments: MONTHLY_PAYMENTS.formInstallmentsValue,
    installmentPeriod: MONTHLY_PAYMENTS.text,
    openEndedStatus: MONTHLY_PAYMENTS.formOpenEndedStatus,
    payFees: DEFAULT_PAY_FEES,
  },
  levelBYearly: {
    bucket: 'levelB',
    amount: (MEMBERSHIP_LEVELS[POSITION_ON_FORM_1].amount / YEARLY_PAYMENT.installmentsPerYear).toString(),
    installments: YEARLY_PAYMENT.formInstallmentsValue,
    installmentPeriod: YEARLY_PAYMENT.text,
    openEndedStatus: YEARLY_PAYMENT.formOpenEndedStatus,
    payFees: DEFAULT_PAY_FEES,
  },
  levelBOneTime: {
    bucket: 'levelB',
    amount: (MEMBERSHIP_LEVELS[POSITION_ON_FORM_1].amount / ONETIME_PAYMENT.installmentsPerYear).toString(),
    installments: ONETIME_PAYMENT.formInstallmentsValue,
    installmentPeriod: ONETIME_PAYMENT.text,
    openEndedStatus: ONETIME_PAYMENT.formOpenEndedStatus,
    payFees: DEFAULT_PAY_FEES,
  },
  levelCMonthly: {
    bucket: 'levelC',
    amount: Math.round(MEMBERSHIP_LEVELS[POSITION_ON_FORM_2].amount / MONTHLY_PAYMENTS.installmentsPerYear).toString(),
    installments: MONTHLY_PAYMENTS.formInstallmentsValue,
    installmentPeriod: MONTHLY_PAYMENTS.text,
    openEndedStatus: MONTHLY_PAYMENTS.formOpenEndedStatus,
    payFees: DEFAULT_PAY_FEES,
  },
  levelCYearly: {
    bucket: 'levelC',
    amount: (MEMBERSHIP_LEVELS[POSITION_ON_FORM_2].amount / YEARLY_PAYMENT.installmentsPerYear).toString(),
    installments: YEARLY_PAYMENT.formInstallmentsValue,
    installmentPeriod: YEARLY_PAYMENT.text,
    openEndedStatus: YEARLY_PAYMENT.formOpenEndedStatus,
    payFees: DEFAULT_PAY_FEES,
  },
  levelCOneTime: {
    bucket: 'levelC',
    amount: (MEMBERSHIP_LEVELS[POSITION_ON_FORM_2].amount / ONETIME_PAYMENT.installmentsPerYear).toString(),
    installments: ONETIME_PAYMENT.formInstallmentsValue,
    installmentPeriod: ONETIME_PAYMENT.text,
    openEndedStatus: ONETIME_PAYMENT.formOpenEndedStatus,
    payFees: DEFAULT_PAY_FEES,
  },
};
//
// MASTER Setting for default selection
// Currently donation level is not a query parameter
//
export const DEFAULT_DONATION_LEVEL_WITH_INSTALL_PERIOD = 'levelAYearly';
export const DEFAULT_ONCE_DONATION_LEVEL_WITH_INSTALL_PERIOD = 'levelAOneTime';

// Texas will be default selection on state list
export const DEFAULT_STATE_SELECTED = 'TX'; // Texas
//
// Whitelisting and query params
// Add new query parameters here to whitelist them
//
export const WL_DEFAULT_QUERY_PARAMETERS = {
  campaignId: '',
  referralId: '',
  installments: BUSINESS_BUCKETS[DEFAULT_DONATION_LEVEL_WITH_INSTALL_PERIOD].installments,
  installmentPeriod: BUSINESS_BUCKETS[DEFAULT_DONATION_LEVEL_WITH_INSTALL_PERIOD].installmentPeriod,
  // Special processing for these
  // (looks redundant but this is per backend and requestor requirements
  installment_period: BUSINESS_BUCKETS[DEFAULT_DONATION_LEVEL_WITH_INSTALL_PERIOD].installmentPeriod,
  openended_status: BUSINESS_BUCKETS[DEFAULT_DONATION_LEVEL_WITH_INSTALL_PERIOD].openEndedStatus,
};
export const WL_QUERY_ESCAPE_THRESHOLD = 6;
