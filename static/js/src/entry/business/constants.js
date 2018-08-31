// eslint-disable-next-line import/prefer-default-export
const TITLE_TEXT = "Business Membership";
const DEFAULT_PAY_FEES = 'True';
const TEXT_FOR_ANNUAL_PAYMENTS = 'yearly';

export const POSITION_IN_PAGE_A = 0;
export const POSITION_IN_PAGE_B = 1;
export const POSITION_IN_PAGE_C = 2;

export const DONATION_LEVELS = [
  { header: 'Supporter', amount: '500' },
  { header: 'Advocate', amount: '1250' },
  { header: 'Hero', amount: '2500' },
];

export const BUSINESS_BUCKETS = {
  levelAYearly: {
    bucket: 'levelA',
    header: DONATION_LEVELS[POSITION_IN_PAGE_A].header,
    amount: DONATION_LEVELS[POSITION_IN_PAGE_A].amount,
    installmentPeriod: TEXT_FOR_ANNUAL_PAYMENTS,
    installments: '3',
    payFees: DEFAULT_PAY_FEES,
  },
  levelBYearly: {
    bucket: 'levelB',
    header: DONATION_LEVELS[POSITION_IN_PAGE_B].header,
    amount: DONATION_LEVELS[POSITION_IN_PAGE_B].amount,
    installmentPeriod: TEXT_FOR_ANNUAL_PAYMENTS,
    installments: '3',
    payFees: DEFAULT_PAY_FEES,
  },
  levelCYearly: {
    position: 2,
    bucket: 'levelC',
    header: DONATION_LEVELS[POSITION_IN_PAGE_C].header,
    amount: DONATION_LEVELS[POSITION_IN_PAGE_C].amount,
    installmentPeriod: TEXT_FOR_ANNUAL_PAYMENTS,
    installments: '3',
    payFees: DEFAULT_PAY_FEES,
  },
};

