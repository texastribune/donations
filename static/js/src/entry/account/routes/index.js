import Home from './home/Index.vue';
import HomeExact from './home-exact/Index.vue';
import Membership from './membership/Index.vue';
import Payments from './payments/Index.vue';
import Blast from './blast/Index.vue';
import BlastPayments from './blast-payments/Index.vue';
import LoggedIn from './logged-in/Index.vue';
import LoggedOut from './logged-out/Index.vue';

const routes = [
  {
    path: '/logged-in/',
    name: 'logged-in',
    component: LoggedIn,
    pathToRegexpOptions: { strict: true },
  },
  {
    path: '/logged-out/',
    name: 'logged-out',
    component: LoggedOut,
    pathToRegexpOptions: { strict: true },
  },
  {
    path: '/',
    component: Home,
    children: [
      {
        path: '',
        name: 'home',
        component: HomeExact,
      },
      {
        path: 'membership/',
        name: 'membership',
        component: Membership,
        pathToRegexpOptions: { strict: true },
      },
      {
        path: 'payments/',
        name: 'payments',
        component: Payments,
        pathToRegexpOptions: { strict: true },
      },
      {
        path: 'blast/',
        name: 'blast',
        component: Blast,
        pathToRegexpOptions: { strict: true },
      },
      {
        path: 'blast-payments/',
        name: 'blast-payments',
        component: BlastPayments,
        pathToRegexpOptions: { strict: true },
      },
      { path: '*', name: 'not-found', redirect: { name: 'home' } },
    ],
  },
];

export default routes;
