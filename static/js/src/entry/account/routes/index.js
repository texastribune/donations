import Home from './home/Index.vue';

const HomeExact = () =>
  import(/* webpackChunkName: "home-exact-route" */ './home-exact/Index.vue');
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

const routes = [
  {
    path: '/logged-in/',
    name: 'logged-in',
    component: LoggedIn,
    pathToRegexpOptions: { strict: true },
    meta: { isProtected: false },
  },
  {
    path: '/logged-out/',
    name: 'logged-out',
    component: LoggedOut,
    pathToRegexpOptions: { strict: true },
    meta: { isProtected: false },
  },
  {
    path: '/',
    component: Home,
    pathToRegexpOptions: { strict: true },
    meta: { isProtected: true },
    children: [
      {
        path: '',
        name: 'home',
        component: HomeExact,
        pathToRegexpOptions: { strict: true },
        meta: { isProtected: true },
      },
      {
        path: 'membership/',
        name: 'membership',
        component: Membership,
        pathToRegexpOptions: { strict: true },
        meta: { isProtected: true },
      },
      {
        path: 'payments/',
        name: 'payments',
        component: Payments,
        pathToRegexpOptions: { strict: true },
        meta: { isProtected: true },
      },
      {
        path: 'blast/',
        name: 'blast',
        component: Blast,
        pathToRegexpOptions: { strict: true },
        meta: { isProtected: true },
      },
      {
        path: 'blast-payments/',
        name: 'blast-payments',
        component: BlastPayments,
        pathToRegexpOptions: { strict: true },
        meta: { isProtected: true },
      },
      { path: '*', name: 'not-found', redirect: { name: 'home' } },
    ],
  },
];

export default routes;
