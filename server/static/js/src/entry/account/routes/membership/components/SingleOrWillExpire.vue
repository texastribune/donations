<template>
  <section class="c-detail-box">
    <div class="has-xxl-btm-marg">
      <info-list :items="data">
        <template #text="{ item: { extra, key } }">
          <template v-if="key === 'donation'">
            {{ extra.amount | currency }},
            {{ extra.lastTransactionDate | longDate }}
          </template>
          <template v-if="key === 'payment'">
            {{ extra.brand }} ending in {{ extra.last4 }}
          </template>
          <template v-if="key === 'status'">
            Your membership is good through
            {{ extra.membershipExpirationDate | longDate }}.
          </template>
        </template>
      </info-list>
    </div>

    <user-internal-nav show-become-sustaining show-donation-history />
  </section>
</template>

<script>
import InfoList from '../../../components/InfoList.vue';

export default {
  name: 'MembershipSingleOrWillExpire',

  components: { InfoList },

  props: {
    lastTransaction: {
      type: Object,
      required: true,
    },

    membershipExpirationDate: {
      type: String,
      required: true,
    },
  },

  computed: {
    data() {
      const data = [];
      const { membershipExpirationDate } = this;
      const { amount, card, date: lastTransactionDate } = this.lastTransaction;

      data.push({
        key: 'donation',
        heading: 'Donation',
        extra: { amount, lastTransactionDate },
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
        extra: { membershipExpirationDate },
      });

      return data;
    },
  },
};
</script>
