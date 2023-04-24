<template>
  <section class="c-detail-box">
    <div class="has-xxl-btm-marg">
      <p
        v-if="failureMessage"
        role="alert"
        class="has-b-btm-marg has-text-error"
      >
        <strong>{{ failureMessage }}</strong>
      </p>
      <p
        v-if="successMessage"
        role="alert"
        class="has-b-btm-marg has-text-success"
      >
        <strong>{{ successMessage }}</strong>
      </p>
      <info-list :items="data">
        <template #text="{ item: { extra, key } }">
          <template v-if="key === 'donation'">
            {{ extra.amount | currency }}, {{ extra.period }}
          </template>
          <template v-if="key === 'payment'">
            {{ extra.brand }} ending in {{ extra.last4 }}
            <div>
              <button @click="togglePaymentForm" class="has-text-teal">
                <span v-if="!openPaymentForm">
                  Edit
                  <icon name="pencil-fill" :display="{ size: 'xs', color: 'teal' }" />
                </span>
                <span v-if="openPaymentForm">
                  Close
                  <icon name="close" :display="{ size: 'xs', color: 'teal' }" />
                </span>
              </button>
            </div>
            <card-update
              v-if="openPaymentForm"
              :stripeCustomerId="extra.stripeCustomerId"
              @formSubmitted="formSubmitted"
              @onSuccess="onSuccess"
              @onFailure="onFailure"
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
      successMessage: '',
      failureMessage: '',
      declinedCard: false,
    }
  },

  computed: {
    data() {
      const data = [];
      const {
        amount,
        period,
        card,
        stripeCustomerId,
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
          extra: { brand, last4, stripeCustomerId },
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
    togglePaymentForm() {
      this.openPaymentForm = !this.openPaymentForm;
      const gaCardBase = {
        event: this.ga.customEventName,
        gaCategory: this.ga.userPortal.category,
        gaLabel: this.ga.userPortal.labels['update-card'],
      };
      if (this.openPaymentForm) {
        window.dataLayer.push({
          ...gaCardBase,
          gaAction: this.ga.userPortal.actions['attempt-card-update'],
        });
      } else {
        window.dataLayer.push({
          ...gaCardBase,
          gaAction: this.ga.userPortal.actions['cancel-card-update'],
        });
      }
    },
  
    formSubmitted() {
      this.successMessage = '';
      this.declinedCard = false;
    },
  
    onSuccess(message) {
      this.successMessage = message;
      this.openPaymentForm = false;
    },
  
    onFailure(message) {
      this.failureMessage = message;
      this.openPaymentForm = false;
    }
  }
};
</script>
