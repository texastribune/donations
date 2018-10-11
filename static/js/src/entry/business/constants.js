// eslint-disable-next-line import/prefer-default-export
export const POSITION_0 = 0;
export const POSITION_1 = 1;
export const POSITION_2 = 2;
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
// Whitelisting and query params
// Add new query parameters here to whitelist them
//
export const WL_DEFAULT_QUERY_PARAMETERS = {
  campaignId: '',
  referralId: '',
  installments: QUERY_PARAMETERS_STRING_VALUES.noneStr,
  installmentPeriod: QUERY_PARAMETERS_STRING_VALUES.monthlyStr,
  // Special processing for these
  // (looks redundant but this is per backend and requestor requirements
  installment_period: QUERY_PARAMETERS_STRING_VALUES.monthlyStr,
  openended_status: QUERY_PARAMETERS_STRING_VALUES.openStr,
};
export const WL_QUERY_ESCAPE_THRESHOLD = 6;

const DEFAULT_PAY_FEES = 'True';

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
export const BUSINESS_BUCKETS = {
  levelAMonthly: {
    bucket: 'levelA',
    amount: Math.round(MEMBERSHIP_LEVELS[POSITION_0].amount / MONTHLY_PAYMENTS.installmentsPerYear),
    // paymentDetails: MONTHLY_PAYMENTS
    installments: MONTHLY_PAYMENTS.formInstallmentsValue,
    installmentPeriod: MONTHLY_PAYMENTS.text,
    openEndedStatus: MONTHLY_PAYMENTS.formOpenEndedStatus,
    payFees: DEFAULT_PAY_FEES,
  },
  levelAYearly: {
    bucket: 'levelA',
    amount: MEMBERSHIP_LEVELS[POSITION_0].amount / YEARLY_PAYMENT.installmentsPerYear,
    installments: YEARLY_PAYMENT.formInstallmentsValue,
    installmentPeriod: YEARLY_PAYMENT.text,
    openEndedStatus: YEARLY_PAYMENT.formOpenEndedStatus,
    payFees: DEFAULT_PAY_FEES,
  },
  levelAOneTime: {
    bucket: 'levelA',
    amount: MEMBERSHIP_LEVELS[POSITION_0].amount / ONETIME_PAYMENT.installmentsPerYear,
    installments: ONETIME_PAYMENT.formInstallmentsValue,
    installmentPeriod: ONETIME_PAYMENT.text,
    openEndedStatus: ONETIME_PAYMENT.formOpenEndedStatus,
    payFees: DEFAULT_PAY_FEES,
  },
  levelBMonthly: {
    bucket: 'levelB',
    amount: Math.round(MEMBERSHIP_LEVELS[POSITION_1].amount / MONTHLY_PAYMENTS.installmentsPerYear),
    installments: MONTHLY_PAYMENTS.formInstallmentsValue,
    installmentPeriod: MONTHLY_PAYMENTS.text,
    openEndedStatus: MONTHLY_PAYMENTS.formOpenEndedStatus,
    payFees: DEFAULT_PAY_FEES,
  },
  levelBYearly: {
    bucket: 'levelB',
    amount: MEMBERSHIP_LEVELS[POSITION_1].amount,
    installments: YEARLY_PAYMENT.formInstallmentsValue,
    installmentPeriod: YEARLY_PAYMENT.text,
    openEndedStatus: YEARLY_PAYMENT.formOpenEndedStatus,
    payFees: DEFAULT_PAY_FEES,
  },
  levelBOneTime: {
    bucket: 'levelB',
    amount: MEMBERSHIP_LEVELS[POSITION_1].amount / ONETIME_PAYMENT.installmentsPerYear,
    installments: ONETIME_PAYMENT.formInstallmentsValue,
    installmentPeriod: ONETIME_PAYMENT.text,
    openEndedStatus: ONETIME_PAYMENT.formOpenEndedStatus,
    payFees: DEFAULT_PAY_FEES,
  },
  levelCMonthly: {
    bucket: 'levelC',
    amount: Math.round(MEMBERSHIP_LEVELS[POSITION_2].amount / MONTHLY_PAYMENTS.installmentsPerYear),
    installments: MONTHLY_PAYMENTS.formInstallmentsValue,
    installmentPeriod: MONTHLY_PAYMENTS.text,
    openEndedStatus: MONTHLY_PAYMENTS.formOpenEndedStatus,
    payFees: DEFAULT_PAY_FEES,
  },
  levelCYearly: {
    bucket: 'levelC',
    amount: MEMBERSHIP_LEVELS[POSITION_2].amount,
    installments: YEARLY_PAYMENT.formInstallmentsValue,
    installmentPeriod: YEARLY_PAYMENT.text,
    openEndedStatus: YEARLY_PAYMENT.formOpenEndedStatus,
    payFees: DEFAULT_PAY_FEES,
  },
  levelCOneTime: {
    bucket: 'levelC',
    amount: MEMBERSHIP_LEVELS[POSITION_2].amount / ONETIME_PAYMENT.installmentsPerYear,
    installments: ONETIME_PAYMENT.formInstallmentsValue,
    installmentPeriod: ONETIME_PAYMENT.text,
    openEndedStatus: ONETIME_PAYMENT.formOpenEndedStatus,
    payFees: DEFAULT_PAY_FEES,
  },
};
//
// Selected box on Choices form
// Currently donation level is not a query parameter, do the one-time
// payment option switched radio selections within the default level
//
export const DEFAULT_DONATION_LEVEL = 'levelAMonthly';
export const DEFAULT_ONCE_DONATION_LEVEL = 'levelAOneTime';

// Texas will be default slection on state list
export const DEFAULT_STATE_SELECTED = 43; // Texas

