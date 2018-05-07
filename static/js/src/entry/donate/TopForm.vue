<template>
  <form
    ref="form"
    action="/charge"
    method="post"
    @submit="onSubmit"
  >
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
    <hidden
      name="openended_status"
      store-module="baseForm"
    />
    <hidden
      name="pay_fees_value"
      store-module="baseForm"
    />
    <pay-fees
      :update-callback="onFeeChange"
      store-module="baseForm"
      amount-store-module="baseForm"
    />
    <level
      amount-store-module="baseForm"
      installment-period-store-module="baseForm"
    />
    <hidden
      name="openended_status"
      store-module="baseForm"
    />
    <token
      :token="token"
    />
    <stripe
      @setToken="setToken"
    />
  </form>
</template>

<script>
import Hidden from '../../elements/Hidden.vue';
import Radios from '../../elements/Radios.vue';
import Level from '../../elements/Level.vue';
import PayFees from '../../elements/PayFees.vue';
import TextInput from '../../elements/TextInput.vue';
import Token from '../../elements/Token.vue';
import Stripe from '../../elements/Stripe.vue';
import replaceSingleValue from '../../mixins/replaceSingleValue';

export default {
  name: 'TopForm',

  components: {
    Hidden,
    TextInput,
    Radios,
    PayFees,
    Level,
    Stripe,
    Token,
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
