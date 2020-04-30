<template>
  <section class="c-detail-box">
    <div class="has-xxl-btm-marg">
      <info-list :items="data">
        <template v-slot:text="{ item: { extra, key } }">
          <template v-if="key === 'donation'">
            {{ extra.amount | currency }}, {{ extra.period }}
          </template>
          <template v-if="key === 'payment'">
            {{ extra.brand }} ending in {{ extra.last4 }}
          </template>
          <template v-if="key === 'next'">
            {{ extra.nextTransactionDate | longDate }}
          </template>
        </template>
      </info-list>
    </div>

    <user-internal-nav show-donation-history />
  </section>
</template>

<script>
import InfoList from '../../../components/InfoList.vue';

export default {
  name: 'MembershipRecurringOrCircle',

  components: { InfoList },

  props: {
    nextTransaction: {
      type: Object,
      required: true,
    },
  },

  computed: {
    data() {
      const data = [];
      const {
        amount,
        period,
        card,
        date: nextTransactionDate,
      } = this.nextTransaction;

      data.push({
        key: 'donation',
        heading: 'Donation',
        extra: { amount, period },
      });

      if (card) {
        const { brand, last4 } = card;

        data.push({
          key: 'payment',
          heading: 'Payment method',
          extra: { brand, last4 },
        });
      }

      data.push({
        key: 'next',
        heading: 'Next payment',
        extra: { nextTransactionDate },
      });

      return data;
    },
  },
};
</script>
