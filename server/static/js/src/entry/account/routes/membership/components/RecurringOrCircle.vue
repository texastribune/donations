<template>
  <section class="c-detail-box">
    <div class="has-xxl-btm-marg">
      <table class="c-table l-width-full">
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
                <div v-if="rdo.type != 'Giving Circle'">
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
    <card-update
      :rdo="stagedRdo"
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
      :link="messageLink"
      :linkText="messageLinkText"
      @onClose="onClose('messageModal')" />
  </section>
</template>

<script>
import { USER_TYPES, CONTEXT_TYPES } from '../../../store/types';

import userMixin from '../../../store/user/mixin';
import contextMixin from '../../../store/context/mixin';

import logError from '../../../utils/log-error';
import { AxiosError } from '../../../errors';

import CardUpdate from './CardUpdate.vue';
import ConfirmModal from '../../../components/ConfirmModal.vue';
import MessageModal from '../../../components/MessageModal.vue';

export default {
  name: 'MembershipRecurringOrCircle',

  components: {
    CardUpdate,
    ConfirmModal,
    MessageModal,
  },

  mixins: [contextMixin, userMixin],

  props: {
    firstName: {
      type: String,
      required: true,
    },
    lastName: {
      type: String,
      required: true,
    },
    email: {
      type: String,
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
      confirmHeading: '',
      confirmBody: '',
      messageHeading: '',
      messageBody: '',
      messageType: '',
      messageLink: '',
      messageLinkText: '',
      checkModalResolve: () => {},
      stagedRdo: {},
    }
  },

  methods: {
    togglePaymentForm(rdo) {
      window.dataLayer.push({
        event: 'customUserPortalEditPaymentIntent',
        gaAction: this.ga.userPortal.actions['attempt-card-update'],
        gaLabel: this.ga.userPortal.labels['update-card'],
      });

      this.stagedRdo = rdo;
      this.$modal.show('cardModal');
    },
  
    onSuccess(message) {
      window.dataLayer.push({
        event: 'customUserPortalEditPaymentSuccess',
        gaAction: this.ga.userPortal.actions['successful-card-update'],
        gaLabel: this.ga.userPortal.labels['update-card'],
      });
      this.messageHeading = "We've updated your payment info"
      this.messageBody = message;
      this.messageType = 'success';
      this.messageLink = '';
      this.messageLinkText = '';
      this.$modal.hide('cardModal');
      this.$modal.show('messageModal');
    },
  
    onFailure(message) {
      this.messageHeading = "We weren't able to update your payment info";
      this.messageBody = message;
      this.messageType = 'failure';
      this.messageLink = '';
      this.messageLinkText = '';
      this.$modal.hide('cardModal');
      this.$modal.show('messageModal');
    },

    onClose(modal) {
      this.$modal.hide(modal);
    },

    async cancelDonation(rdo) {
      window.dataLayer.push({
        event: 'customUserPortalCancelIntent',
        gaAction: this.ga.userPortal.actions['attempt-cancel-donation'],
        gaLabel: this.ga.userPortal.labels['cancel-donation'],
      });

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
          window.dataLayer.push({
            event: 'customUserPortalCancelSuccess',
            gaAction: this.ga.userPortal.actions['successful-cancel-donation'],
            gaLabel: this.ga.userPortal.labels['cancel-donation'],
          });
          this.messageHeading = "We've cancelled your recurring donation";
          this.messageBody = `<div class="t-size-s">Your ${rdo.period} donation of $${rdo.amount} has been cancelled.</div>
                              <hr class="has-b-btm-marg"/>
                              <div class="has-b-btm-marg">We're sorry to see you go! Can you let us know why?</div>`;
          this.messageType = 'success';
          this.messageLink = `https://airtable.com/appmeSLgv6yUW4HcC/shraO409FOodYJs68?prefill_First+name=${this.firstName}&prefill_Last+name=${this.lastName}&prefill_Email=${this.email}`;
          this.messageLinkText = "Share your feedback";
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
              this.messageBody = 'An internal error occurred. Please try again and if the issue persists, contact us at membership@texastribune.org'
            }
            else if (
              err.extra.data.detail === "invalid card"
            ) {
              this.messageBody = 'The submitted card was declined or invalid. Please check your information and resubmit'
            }
            this.messageHeading = "We weren't able to cancel your donation";
            this.messageType = 'failure';
            this.messageLink = '';
            this.messageLinkText = '';
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
