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
    path: '/logged-in',
    name: 'logged-in',
    component: LoggedIn,
    meta: { title: 'Logged In' },
  },
  {
    path: '/logged-out',
    name: 'logged-out',
    component: LoggedOut,
    meta: { title: 'Logged Out' },
  },
  {
    path: '/',
    component: Home,
    children: [
      {
        path: '',
        name: 'home',
        component: HomeExact,
        meta: { title: 'Home' },
      },
      {
        path: 'membership',
        name: 'membership',
        component: Membership,
        meta: { title: 'Membership' },
      },
      {
        path: 'payments',
        name: 'payments',
        component: Payments,
        meta: { title: 'Donation History' },
      },
      {
        path: 'blast',
        name: 'blast',
        component: Blast,
        meta: { title: 'The Blast' },
      },
      {
        path: 'blast-payments',
        name: 'blast-payments',
        component: BlastPayments,
        meta: { title: 'The Blast Payment History' },
      },
      { path: '*', name: 'not-found', redirect: { name: 'home' } },
    ],
  },
];

export default routes;
