<template>
  <donate-form
    :initial-fields="initialFields"
    :show-success="showSuccess"
    @onSubmit="buildDispatches"
  />
</template>

<script>
import userMixin from '../../../store/user/mixin';
import tokenUserMixin from '../../../store/token-user/mixin';
import contextMixin from '../../../store/context/mixin';

import DonateForm from '../components/DonateForm.vue';

import logError from '../../../utils/log-error';

import { AxiosError } from '../../../errors';
import { CONTEXT_TYPES, USER_TYPES } from '../../../store/types';

export default {
  name: 'DonateFormContainer',

  components: { DonateForm },

  mixins: [userMixin, tokenUserMixin, contextMixin],

  data() {
    return { showSuccess: false };
  },

  computed: {
    initialFields() {

      return {
        firstName: '',
        lastName: '',
        email: '',
        installmentPeriod: '',
        amount: '',
        payFees: false,
      };
    },
  },

  methods: {
    resetSuccess(formIsPristine) {
      if (!formIsPristine) {
        this.showSuccess = false;
      }
    },

    buildPaymentInfo(fields) {
      const paymentInfo = {};
      
      paymentInfo.first_name = fields.firstName.value;
      paymentInfo.last_name = fields.lastName.value;
      paymentInfo.installment_period = fields.installmentPeriod.value;
      paymentInfo.amount = fields.amount.value;
      paymentInfo.email = fields.email.value;
      paymentInfo.pay_fees = fields.payFees.value;

      return paymentInfo;
    },

    async buildDispatches(fields) {
      const dispatches = [];
      const paymentInfo = this.buildPaymentInfo(fields);

      dispatches.push(this[USER_TYPES.createDonation](paymentInfo));
      
      await this.createPayment(dispatches);
    },

    async createPayment(dispatches) {
      this[CONTEXT_TYPES.setIsFetching](true);

      try {
        await Promise.all(dispatches);
      } catch (err) {
        if (
          err instanceof AxiosError &&
          err.status === 400
        ) {
          logError({ err, level: 'warning' });
        } else {
          throw err;
        }
      }

      this.showSuccess = true;

      this[CONTEXT_TYPES.setIsFetching](false);
    },
  },
};
</script>
