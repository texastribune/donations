<template>
  <section class="c-detail-box">
    <div class="has-xxl-btm-marg">
      <p
        v-if="successMessage"
        role="alert"
        class="has-b-btm-marg has-text-success"
      >
        <strong>{{successMessage}}</strong>
      </p>
      <info-list :items="data">
        <template #text="{ item: { extra, key } }">
          <template v-if="key === 'donation'">
            {{ extra.amount | currency }}, {{ extra.period }}
          </template>
          <template v-if="key === 'payment'">
            {{ extra.brand }} ending in {{ extra.last4 }}
            <button @click="openPaymentForm = !openPaymentForm">
              <icon v-if="!openPaymentForm" name="pencil-fill" :display="{ size: 's' }" />
              <icon v-if="openPaymentForm" name="close" :display="{ size: 's' }" />
            </button>
            <card-update
              v-if="openPaymentForm"
              @onSuccess="onSuccess"
            ></card-update>
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
import CardUpdate from './CardUpdate.vue';

export default {
  name: 'MembershipRecurringOrCircle',

  components: { InfoList, CardUpdate },

  props: {
    nextTransaction: {
      type: Object,
      required: true,
    },
  },

  data() {
    return {
      openPaymentForm: false,
      successMessage: ''
    }
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

  methods: {
    onSuccess(message, last4) {
      this.successMessage = message;
      this.openPaymentForm = false;
    }
  }
};
</script>
