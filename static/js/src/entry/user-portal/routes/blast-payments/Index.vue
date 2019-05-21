<template>
  <div class="has-bg-white has-ump-top-padding">
    <h1 class="has-xxl-btm-marg has-ump-side-padding">
      The Blast Newsletter: Payment History
    </h1>

    <div class="has-ump-side-padding has-xxl-btm-marg">
      <section class="c-detail-box">
        <payment-list :payments="payments" />
      </section>
    </div>

    <appeal />

    <help blast />
  </div>
</template>

<script>
import routeMixin from '../../mixins/route';
import routeFetchMixin from '../../mixins/route-fetch';
import PaymentList from '../../components/PaymentList.vue';
import Appeal from '../../components/Appeal.vue';
import Help from '../../components/Help.vue';

export default {
  name: 'Index',

  components: { Appeal, PaymentList, Help },

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
