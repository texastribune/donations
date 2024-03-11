/* eslint-disable prefer-destructuring */
export const READ_WRITE_CREDIT_CARD_MESSAGE_KEY = 'readWriteCreditCardMessage';
export const READ_WRITE_WELCOME_MESSAGE_KEY = 'readWriteWelcomeMessage';
export const NON_STAFF_CONNECTION = 'Username-Password-Authentication';
export const PORTAL_API_URL = `${process.env.PORTAL_API_DOMAIN}/v1/`;
export const DONATE_URL = `/donate?installmentPeriod=monthly&amount=15&campaignId=${process.env.PORTAL_CAMPAIGN_ID}#join-today`;
export const CIRCLE_URL = '/circle';
export const AUTH_DOMAIN = process.env.AUTH0_DOMAIN;
export const AUTH_PORTAL_AUDIENCE = process.env.AUTH0_PORTAL_AUDIENCE;
export const AUTH_PORTAL_CLIENT_ID = process.env.AUTH0_PORTAL_CLIENT_ID;
export const AUTH_PORTAL_LOGOUT_COMPLETE_URL = `${window.location.origin}/account/logged-out/`;
export const AUTH_PORTAL_LOGIN_COMPLETE_URL = `${window.location.origin}/account/logged-in/`;
export const TITLE_SUFFIX = ' | Your Texas Tribune Account';
export const SENTRY_DSN = process.env.SENTRY_DSN;
export const SENTRY_ENVIRONMENT = process.env.SENTRY_ENVIRONMENT;
export const ENABLE_SENTRY = process.env.ENABLE_SENTRY.toLowerCase() === 'true';
export const GA_USER_PORTAL_NAV = {
  category: 'user portal navigation',
  actions: {
    side: 'side nav click',
    top: 'top nav click',
    footer: 'footer link click',
    inline: 'inline link click',
  },
  labels: {
    home: 'account overview',
    membership: 'membership overview',
    payments: 'donation history',
    blast: 'the blast overview',
    'blast-payments': 'the blast payment history',
    'edit-contact-info': 'profile editor',
    'confirm-linked-identity': 'link email confirmation',
    // external starting here
    'community-guidelines': 'community guidelines',
    'support-landing': 'support landing',
    'privacy-policy': 'privacy policy',
    'texas-tribune-home': 'texas tribune home',
    'circle-landing': 'circle landing',
    'donor-wall': 'donor wall',
  },
};
export const GA_USER_PORTAL = {
  category: 'user portal',
  actions: {
    'reset-password': 'reset password',
    'contact-us': 'contact us',
    'tax-receipt': 'download tax receipt',
    'blast-receipt': 'download blast receipt',
    'clear-notification': 'clear notification',
    'submit-linked-email': 'lookup linked email',
    'confirm-linked-email': 'confirm linked email',
    'cancel-linked-email': 'cancel linked email',
    'login-linked-email': 'login linked email',
    'edit-name': 'edit name',
    'edit-email': 'edit account email',
    'edit-zip': 'edit zip',
    'marketing-opt-in': 'marketing opt-in',
    'marketing-opt-out': 'marketing opt-out',
    'attempt-card-update': 'attempt credit card update',
    'successful-card-update': 'successful credit card update',
    'attempt-cancel-donation': 'attempt donation cancellation',
    'successful-cancel-donation': 'successful donation cancellation',
  },
  labels: {
    home: 'account overview',
    membership: 'membership overview',
    payments: 'donation history',
    blast: 'the blast overview',
    error: 'error page',
    unverified: 'unverified page',
    'blast-payments': 'the blast payment history',
    'edit-contact-info': 'profile editor',
    'confirm-linked-identity': 'link email confirmation',
    'login-linked-identity': 'link email login',
    'changed-email': 'changed email confirmation',
    'update-card': 'update credit card',
    'cancel-donation': 'cancel recurring donation',
  },
};
export const GA_DONATIONS = {
  category: 'donations',
  actions: {
    'membership-intent': 'membership-intent',
  },
  labels: {
    'upgrade-membership': 'user portal - become a sustainer',
    'renew-membership': 'user portal - renew',
    'upgrade-contact': 'user portal - contact to upgrade',
    'never-given': 'user portal - never given',
    top: 'user portal - top nav click',
    footer: 'user portal - footer link click',
  },
};
export const GA_BLAST_INTENT = {
  category: 'blast intent',
  actions: {
    'renew-blast': 'user portal - renew link',
  },
  labels: {
    'user-portal': 'user portal',
  },
};
export const GA_CUSTOM_EVENT_NAME = 'customUserPortal';
export const REDIRECTS_META = {
  donate: {
    external: true,
    url: '/donate',
  },
  accountOverview: {
    external: false,
    routeName: 'accountOverview',
  },
  confirmLinkedIdentity: {
    external: false,
    routeName: 'confirm-linked-identity',
  },
  changedEmail: {
    external: false,
    routeName: 'changed-email',
  },
};
