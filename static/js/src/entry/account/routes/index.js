import store from '../store';
import { USER_MODULE, USER_TYPES } from '../store/types';
import Home from './home/Index.vue';

const HomeExact = () =>
  import(/* webpackChunkName: "home-exact-route" */ './home-exact/Index.vue');
const EditContactInfo = () =>
  import(/* webpackChunkName: "edit-contact-info-route" */ './edit-contact-info/Index.vue');
const Ambassador = () =>
  import(/* webpackChunkName: "ambassador-route" */ './ambassador/Index.vue');
const Membership = () =>
  import(/* webpackChunkName: "membership-route" */ './membership/Index.vue');
const Payments = () =>
  import(/* webpackChunkName: "payments-route" */ './payments/Index.vue');
const Blast = () =>
  import(/* webpackChunkName: "blast-route" */ './blast/Index.vue');
const BlastPayments = () =>
  import(/* webpackChunkName: "blast-payments-route" */ './blast-payments/Index.vue');
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
    component: Home,
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
        name: 'home',
        component: HomeExact,
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
        path: 'ambassador/',
        name: 'ambassador',
        component: Ambassador,
        pathToRegexpOptions: { strict: true },
        meta: {
          isProtected: true,
          title: 'Refer a Friend',
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
          return next({ name: 'home' });
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
          return next({ name: 'home' });
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
          return next({ name: 'home' });
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
          return next({ name: 'home' });
        },
      },
      { path: '*', name: 'not-found', redirect: { name: 'home' } },
    ],
  },
];

export default routes;
