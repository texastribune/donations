<template>
  <section class="c-detail-box c-detail-box--from-l">
    <div class="has-xxxl-btm-marg">
      <info-list :items="data">
        <template #text="{ item: { key, extra } }">
          <template v-if="key === 'subscription'">
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

    <user-internal-nav show-blast-payments />
  </section>
</template>

<script>
import InfoList from '../../../components/InfoList.vue';

export default {
  name: 'BlastCurrent',

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
        key: 'subscription',
        heading: 'Subscription',
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
