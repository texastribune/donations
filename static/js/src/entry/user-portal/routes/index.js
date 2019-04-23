import Home from './home/Index.vue';
import Membership from './membership/Index.vue';
import Payments from './payments/Index.vue';
import Blast from './blast/Index.vue';
import BlastPayments from './blast-payments/Index.vue';
import LoggedIn from './logged-in/Index.vue';
import LoggedOut from './logged-out/Index.vue';

const routes = [
  { path: '/logged-in', name: 'logged-in', component: LoggedIn },
  { path: '/logged-out', name: 'logged-out', component: LoggedOut },
  {
    path: '/',
    name: 'home',
    component: Home,
    children: [
      { path: 'membership', name: 'membership', component: Membership },
      { path: 'payments', name: 'payments', component: Payments },
      { path: 'blast', name: 'blast', component: Blast },
      {
        path: 'blast-payments',
        name: 'blast-payments',
        component: BlastPayments,
      },
      { path: '*', name: 'not-found', redirect: { name: 'home' } },
    ],
  },
];

export default routes;
