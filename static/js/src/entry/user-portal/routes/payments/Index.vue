<template>
  <div class="c-top-route">
    <h1>Your Donations</h1>

    <section>
      <payment-list :payments="payments" />
      <ul>
        <li>
          &rarr;&nbsp;
          <router-link :to="{ name: 'membership' }"
            >See your membership status</router-link
          >
        </li>
        <li>&rarr;&nbsp; <a href="">Download your 2018 tax receipt</a></li>
        <li>
          &rarr;&nbsp;
          <a href="/donate#join-today">Become a sustaining member</a>
        </li>
      </ul>
    </section>

    <help membership />
  </div>
</template>

<script>
import routeMixin from '../../mixins/route';
import routeFetchMixin from '../../mixins/route-fetch';
import PaymentList from '../../components/PaymentList.vue';
import Help from '../../components/Help.vue';

export default {
  name: 'Index',

  components: { PaymentList, Help },

  mixins: [routeMixin, routeFetchMixin],

  data() {
    return {
      payments: [
        { id: 0, date: '03/29/18', amount: '$329', method: 'AMEX 8568' },
        { id: 1, date: '03/29/18', amount: '$329', method: 'AMEX 8568' },
        { id: 2, date: '03/29/18', amount: '$329', method: 'AMEX 8568' },
        { id: 3, date: '03/29/18', amount: '$329', method: 'AMEX 8568' },
        { id: 4, date: '03/29/18', amount: '$329', method: 'AMEX 8568' },
      ],
    };
  },

  methods: {
    async fetchData() {
      return null;
    },
  },
};
</script>
