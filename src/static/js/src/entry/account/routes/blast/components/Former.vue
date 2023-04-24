<template>
  <section class="c-detail-box c-detail-box--from-l">
    <div class="has-xxxl-btm-marg">
      <info-list :items="data">
        <template #text="{ item: { key, extra, text } }">
          <template v-if="key === 'subscription'">
            {{ extra.amount | currency }}, {{ extra.period }}
          </template>
          <template v-if="key === 'payment'">
            {{ extra.brand }} ending in {{ extra.last4 }}
          </template>
          <template v-if="key === 'status'">
            {{ text }}
          </template>
        </template>
      </info-list>
    </div>

    <user-internal-nav show-blast-payments show-renew-blast />
  </section>
</template>

<script>
import InfoList from '../../../components/InfoList.vue';

export default {
  name: 'BlastFormer',

  components: { InfoList },

  props: {
    lastTransaction: {
      type: Object,
      required: true,
    },
  },

  computed: {
    data() {
      const data = [];
      const { amount, period, card } = this.lastTransaction;

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
        key: 'status',
        heading: 'Status',
        text: 'Your subscription is no longer active.',
      });

      return data;
    },
  },
};
</script>
