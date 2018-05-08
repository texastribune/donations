<template>
  <form
    ref="form"
    action="/charge"
    method="post"
    @submit="onSubmit"
  >
    <email
      name="stripeEmail"
      store-module="baseForm"
    />
    <text-input
      name="first_name"
      store-module="baseForm"
    />
    <text-input
      name="last_name"
      store-module="baseForm"
    />
    <text-input
      :required="false"
      name="reason"
      store-module="baseForm"
    />
    <text-input
      name="amount"
      store-module="baseForm"
    />
    <radios
      :update-callback="onFrequencyUpdate"
      :options="frequencyOptions"
      name="installment_period"
      store-module="baseForm"
    />
    <text-input
      :required="false"
      pattern="[0-9]{5}"
      name="zipcode"
      store-module="baseForm"
    />
    <pay-fees
      :update-callback="onFeeChange"
      store-module="baseForm"
      amount-store-module="baseForm"
    />
    <basic-pay
      @setToken="setToken"
    />
    <level
      amount-store-module="baseForm"
      installment-period-store-module="baseForm"
    />
    <local-hidden
      :value="token"
      name="stripeToken"
    />
    <connected-hidden
      name="description"
      store-module="baseForm"
    />
    <connected-hidden
      name="campaign_id"
      store-module="baseForm"
    />
    <connected-hidden
      name="openended_status"
      store-module="baseForm"
    />
    <connected-hidden
      name="pay_fees_value"
      store-module="baseForm"
    />
  </form>
</template>

<script>
import ConnectedHidden from '../../connected/Hidden.vue';
import Radios from '../../connected/Radios.vue';
import Level from '../../connected/Level.vue';
import PayFees from '../../connected/PayFees.vue';
import TextInput from '../../connected/TextInput.vue';
import Email from '../../connected/Email.vue';

import LocalHidden from '../../local/Hidden.vue';
import BasicPay from '../../local/BasicPay.vue';

import replaceSingleValue from '../../mixins/replaceSingleValue';

export default {
  name: 'TopForm',

  components: {
    ConnectedHidden,
    LocalHidden,
    TextInput,
    Radios,
    PayFees,
    Level,
    Email,
    BasicPay,
  },

  mixins: [replaceSingleValue],

  data() {
    return {
      frequencyOptions: [
        { id: 0, text: 'monthly', value: 'monthly' },
        { id: 1, text: 'yearly', value: 'yearly' },
        { id: 2, text: 'one time', value: 'None' },
      ],

      token: '',
    };
  },

  methods: {
    onFrequencyUpdate(newValue) {
      let openEndedVal = '';

      if (newValue === 'yearly' ||
          newValue === 'monthly'
      ) {
        openEndedVal = 'Open';
      } else if (newValue === 'None') {
        openEndedVal = 'None';
      }

      this.replaceSingleValue({
        storeModule: 'baseForm',
        name: 'openended_status',
        newValue: openEndedVal,
      });
    },

    onFeeChange(checked) {
      this.replaceSingleValue({
        storeModule: 'baseForm',
        name: 'pay_fees_value',
        newValue: checked ? 'True' : 'False',
      });
    },

    onSubmit(event) {
      event.preventDefault();
    },

    setToken(newToken) {
      this.token = newToken;
    },
  },
};
</script>
