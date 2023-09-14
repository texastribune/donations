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
      <info-list v-if="!canViewAs" :items="data">
        <template #text="{ item: { extra, key } }">
          <template v-if="key === 'donation'">
            {{ extra.amount | currency }}, {{ extra.period }}
          </template>
          <template v-if="key === 'payment'">
            {{ extra.brand }} ending in {{ extra.last4 }}
            <div>
              <button class="has-text-teal" @click="toggleInlinePaymentForm">
                <span v-if="!openPaymentForm">
                  Edit
                  <span class="c-icon c-icon--teal c-icon--baseline t-size-s">
                    <svg aria-hidden="true"><use href="#pencil-fill"></use></svg>
                  </span>
                </span>
                <span v-if="openPaymentForm">
                  Close
                  <span class="c-icon c-icon--teal c-icon--baseline t-size-s">
                    <svg aria-hidden="true"><use href="#close"></use></svg>
                  </span>
                </span>
              </button>
            </div>
            <card-update
              v-if="openPaymentForm"
              :stripe-customer-id="extra.stripeCustomerId"
              @formSubmitted="formSubmitted"
              @onSuccess="onInlineSuccess"
              @onFailure="onInlineFailure"
            ></card-update>
          </template>
          <template v-if="key === 'next'">
            {{ extra.nextTransactionDate | longDate }}
          </template>
        </template>
      </info-list>
      <table v-if="canViewAs" class="c-table l-width-full">
        <thead>
          <tr>
            <th class="t-align-left"><strong>Donation</strong></th>
            <th class="t-align-left"><strong>Payment Method</strong></th>
            <th class="t-align-left"><strong>Next Payment</strong></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="rdo in recurringTransactions" :key="rdo.id">
            <td>
              <slot name="donation" :donation="rdo.period">
                {{ rdo.amount | currency }}, {{ rdo.period }}
              </slot>
            </td>
            <td>
              <slot name="method" :method="rdo.credit_card">
                {{ rdo.credit_card.brand }} ending in {{ rdo.credit_card.last4 }}
                <div>
                  <button
                    aria-label="change card"
                    class="has-text-teal"
                    @click="togglePaymentForm(rdo)"
                  >
                    Edit
                    <span class="c-icon c-icon--teal c-icon--baseline t-size-xs">
                      <svg aria-hidden="true"><use href="#pencil-fill"></use></svg>
                    </span>
                  </button>
                </div>
              </slot>
            </td>
            <td>
              <slot name="next" :next="rdo.next_payment_date">
                {{ rdo.next_payment_date }}
                <div>
                  <button
                    aria-label="cancel subscription"
                    class="has-text-teal"
                    @click="cancelDonation(rdo)"
                  >
                    Cancel
                    <span class="c-icon c-icon--teal c-icon--baseline t-size-xs">
                      <svg aria-hidden="true"><use href="#close"></use></svg>
                    </span>
                  </button>
                </div>
              </slot>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <user-internal-nav show-donation-history />
    <card-update-new
      :rdo="stagedRdo"
      @formSubmitted="formSubmitted"
      @onSuccess="onSuccess"
      @onFailure="onFailure"
      @onClose="onClose('cardModal')" />
    <confirm-modal
      :resolve="checkModalResolve"
      :heading="confirmHeading"
      :message="confirmBody"
      :reject-text="'No'"
      :accept-text="'Yes'" 
      @onClose="onClose('confirmModal')" />
    <message-modal
      :heading="messageHeading"
      :messageType="messageType"
      :messageBody="messageBody" 
      @onClose="onClose('messageModal')" />
  </section>
</template>

<script>
import { USER_TYPES, CONTEXT_TYPES } from '../../../store/types';

import userMixin from '../../../store/user/mixin';
import contextMixin from '../../../store/context/mixin';

import logError from '../../../utils/log-error';
import { AxiosError } from '../../../errors';

import ConfirmModal from '../../../components/ConfirmModal.vue';
import InfoList from '../../../components/InfoList.vue';
import CardUpdateNew from './CardUpdateNew.vue';
import CardUpdate from './CardUpdate.vue';
import MessageModal from '../../../components/MessageModal.vue';

export default {
  name: 'MembershipRecurringOrCircle',

  components: {
    ConfirmModal,
    InfoList,
    CardUpdateNew,
    CardUpdate,
    MessageModal,
  },

  mixins: [contextMixin, userMixin],

  props: {
    nextTransaction: {
      type: Object,
      required: true,
    },
    recurringTransactions: {
      type: Array,
      required: true,
    },
    canViewAs: {
      type: Boolean,
      required: false,
    }
  },

  data() {
    return {
      openPaymentForm: false,
      openConfirmModal: false,
      successMessage: '',
      failureMessage: '',
      confirmHeading: '',
      confirmBody: '',
      messageHeading: '',
      messageBody: '',
      messageType: '',
      declinedCard: false,
      checkModalResolve: () => {},
      stagedRdo: {},
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
    toggleInlinePaymentForm() {
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

    onInlineSuccess(message) {
      this.successMessage = message;
      this.openPaymentForm = false;
    },
  
    onInlineFailure(message) {
      this.failureMessage = message;
      this.openPaymentForm = false;
    },

    togglePaymentForm(rdo) {
      this.stagedRdo = rdo;

      this.$modal.show('cardModal');
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
      this.messageHeading = "We've updated your payment info"
      this.messageBody = message;
      this.messageType = 'success';
      this.$modal.hide('cardModal');
      this.$modal.show('messageModal');
    },
  
    onFailure(message) {
      this.messageHeading = "Credit Card Update Failed";
      this.messageBody = message;
      this.messageType = 'failure';
      this.$modal.hide('cardModal');
      this.$modal.show('messageModal');
    },

    onClose(modal) {
      this.$modal.hide(modal);
    },

    async cancelDonation(rdo) {
      this.updateFailure = false;
      this.confirmHeading = 'Cancel Recurring Donation?';
      this.confirmBody = `<p>By selecting <b>yes</b>, you are canceling your recurring donation
                            and will not be charged at your next scheduled renewal date.
                          </p>`;

      this.$modal.show('confirmModal');

      const shouldCancel = await this.checkModalAction();

      this.$modal.hide('confirmModal');

      if (shouldCancel) {
        this[CONTEXT_TYPES.setIsFetching](true);
        try {
          await this[USER_TYPES.closeRdo]({
            rdoId: rdo.id,
            stripeSubscriptionId: rdo.stripe_subscription_id,
          });
          this.messageHeading='Donation Cancelled Successfully';
          this.messageBody = `<div class="t-size-s">Recurring donation of $${rdo.amount} (${rdo.period}) has been cancelled.</div>
                              <hr/>
                              <div>We're sorry to see you go! Can you let us know why?</div>
                              <base-button
                                :text="'Share your feedback'"
                                :link="'https://airtable.com/appyo1zuQd8f4hBVx/shr6ZCx0OAnhrm1BJ'"
                                :display="{ size: 's' }"
                              />`;
          this.messageType = 'success';
        } catch (err) {
          this.updateFailure = true;
          logError({err, level: 'warning'})

          if (
            err instanceof AxiosError &&
            err.status === 400
          ) {
            if (
              err.extra.data.detail === "missing data"
            ) {
              this.failureMessage = 'An internal error occurred. Please try again and if the issue persists, contact us at membership@texastribune.org'
            }
            else if (
              err.extra.data.detail === "invalid card"
            ) {
              this.failureMessage = 'The submitted card was declined or invalid. Please check your information and resubmit'
            }
            this.messageHeading = "Donation Cancelation Failed";
            this.messageBody = this.failureMessage;
            this.messageType = 'failure';
          }
        }
      this[CONTEXT_TYPES.setIsFetching](false);
      this.$modal.show('messageModal');
      }
    },

    checkModalAction() {
       return new Promise((resolve) => {
         this.checkModalResolve = resolve;
       });
     },
  }
};
</script>
