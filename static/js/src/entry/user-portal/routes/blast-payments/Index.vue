<template>
  <div class="has-bg-white has-ump-top-padding">
    <h1 class="has-l-btm-marg has-ump-side-padding t-size-xl">
      The Blast Newsletter: Payment History
    </h1>

    <div class="has-ump-side-padding has-xxl-btm-marg">
      <section class="c-detail-box">
        <div class="has-xxxl-btm-marg">
          <payment-list :payments="payments" />
        </div>

        <ul class="c-link-list t-linkstyle--underlined">
          <li>
            <span class="c-link-list__arrow has-text-teal">
              <strong>&rarr;</strong>
            </span>
            <router-link :to="{ name: 'blast' }"
              >More about your subscription</router-link
            >
          </li>
        </ul>
      </section>
    </div>

    <help blast :display="{ hasTopPadding: true }" />
  </div>
</template>

<script>
import routeMixin from '../../mixins/route';
import PaymentList from '../../components/PaymentList.vue';
import Help from '../../components/Help.vue';

export default {
  name: 'BlastPaymentsRoute',

  components: { PaymentList, Help },

  mixins: [routeMixin],

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
