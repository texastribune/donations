import store from '../store';

import Account from './account/Index.vue';

import { TOKEN_USER_MODULE, USER_MODULE, USER_TYPES } from '../store/types';

const AccountOverview = () =>
  import(/* webpackChunkName: "account-overview-route" */ './account-overview/Index.vue');
const EditContactInfo = () =>
  import(/* webpackChunkName: "edit-contact-info-route" */ './edit-contact-info/Index.vue');
const Membership = () =>
  import(/* webpackChunkName: "membership-route" */ './membership/Index.vue');
const Payments = () =>
  import(/* webpackChunkName: "payments-route" */ './payments/Index.vue');
const Blast = () =>
  import(/* webpackChunkName: "blast-route" */ './blast/Index.vue');
const BlastPayments = () =>
  import(/* webpackChunkName: "blast-payments-route" */ './blast-payments/Index.vue');
const CreateDonation = () =>
  import(/* webpackChunkName: "create-donation" */ './create-donation/Index.vue');
const LoggedIn = () =>
  import(/* webpackChunkName: "logged-in-route" */ './logged-in/Index.vue');
const LoggedOut = () =>
  import(/* webpackChunkName: "logged-out-route" */ './logged-out/Index.vue');
const ChangedEmail = () =>
  import(/* webpackChunkName: "changed-email-route" */ './changed-email/Index.vue');
const ConfirmLinkedIdentity = () =>
  import(/* webpackChunkName: "confirmed-linked-identity-route" */ './confirm-linked-identity/Index.vue');

const routes = [
  {
    path: '/logged-in/',
    name: 'logged-in',
    component: LoggedIn,
    pathToRegexpOptions: { strict: true },
    meta: {
      isProtected: true,
      title: 'Logged In',
    },
  },
  {
    path: '/logged-out/',
    name: 'logged-out',
    component: LoggedOut,
    pathToRegexpOptions: { strict: true },
    meta: {
      isProtected: false,
      title: 'Logged Out',
    },
  },
  {
    path: '/changed-email/',
    name: 'changed-email',
    component: ChangedEmail,
    pathToRegexpOptions: { strict: true },
    meta: {
      isProtected: false,
      title: 'Verify your changed email',
    },
  },
  {
    path: '/confirm-linked-identity/',
    name: 'confirm-linked-identity',
    component: ConfirmLinkedIdentity,
    pathToRegexpOptions: { strict: true },
    meta: {
      isProtected: false,
      title: 'Confirm linked email address',
    },
  },
  {
    path: '/',
    component: Account,
    pathToRegexpOptions: { strict: true },
    meta: {
      isProtected: true,
      title: null,
      async fetchData() {
        await store.dispatch(`${USER_MODULE}/${USER_TYPES.getUser}`);
      },
    },
    children: [
      {
        path: '',
        name: 'accountOverview',
        component: AccountOverview,
        pathToRegexpOptions: { strict: true },
        meta: {
          isProtected: true,
          title: 'Home',
          requiresParentFetch: false,
        },
      },
      {
        path: 'edit-contact-info/',
        name: 'edit-contact-info',
        component: EditContactInfo,
        pathToRegexpOptions: { strict: true },
        meta: {
          isProtected: true,
          title: 'Your Profile Settings',
          requiresParentFetch: false,
        },
      },
      {
        path: 'membership/',
        name: 'membership',
        component: Membership,
        pathToRegexpOptions: { strict: true },
        meta: {
          isProtected: true,
          title: 'Membership',
          requiresParentFetch: false,
        },
        beforeEnter: (to, from, next) => {
          const hasGivenNotCustom =
            store.getters[`${USER_MODULE}/hasGivenNotCustom`];

          if (hasGivenNotCustom) {
            return next();
          }
          return next({ name: 'accountOverview' });
        },
      },
      {
        path: 'payments/',
        name: 'payments',
        component: Payments,
        pathToRegexpOptions: { strict: true },
        meta: {
          isProtected: true,
          title: 'Donation History',
          requiresParentFetch: false,
        },
        beforeEnter: (to, from, next) => {
          const isNeverGiven = store.getters[`${USER_MODULE}/isNeverGiven`];

          if (!isNeverGiven) {
            return next();
          }
          return next({ name: 'accountOverview' });
        },
      },
      {
        path: 'blast/',
        name: 'blast',
        component: Blast,
        pathToRegexpOptions: { strict: true },
        meta: {
          isProtected: true,
          title: 'The Blast',
          requiresParentFetch: false,
        },
        beforeEnter: (to, from, next) => {
          const isBlastSubscriber =
            store.getters[`${USER_MODULE}/isBlastSubscriber`];

          if (isBlastSubscriber) {
            return next();
          }
          return next({ name: 'accountOverview' });
        },
      },
      {
        path: 'blast-payments/',
        name: 'blast-payments',
        component: BlastPayments,
        pathToRegexpOptions: { strict: true },
        meta: {
          isProtected: true,
          title: 'The Blast Payment History',
          requiresParentFetch: false,
        },
        beforeEnter: (to, from, next) => {
          const isBlastSubscriber =
            store.getters[`${USER_MODULE}/isBlastSubscriber`];

          if (isBlastSubscriber) {
            return next();
          }
          return next({ name: 'accountOverview' });
        },
      },
      {
        path: 'create-donation/',
        name: 'create-donation',
        component: CreateDonation,
        pathToRegexpOptions: { strict: true },
        meta: {
          isProtected: true,
          title: 'Create a New Donation',
          requiresParentFetch: false,
        },
        beforeEnter: (to, from, next) => {
          const administrator =
            store.getters[`${TOKEN_USER_MODULE}/canViewAs`];

          if (administrator) {
            return next();
          }
          return next({ name: 'accountOverview' });
        },
      },
      { path: '*', name: 'not-found', redirect: { name: 'accountOverview' } },
    ],
  },
];

export default routes;
