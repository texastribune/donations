<template>
  <div aria-live="polite">
    <div :class="classes">
      <input
        id="pay-fees"
        :checked="isChecked"
        type="checkbox"
        @change="onChange($event.target.checked)"
      />
      <label for="pay-fees">
        I agree to pay <span v-if="feeAmount">{{ feeAmount }}</span>
        <span>{{ installmentPeriod }}</span> for processing fees. This directs
        more money to our mission.
      </label>
    </div>
  </div>
</template>

<script>
import updateValue from './mixins/update-value';
import getValue from './mixins/get-value';
import { isValidDonationAmount } from '../utils/validators';

export default {
  name: 'PayFees',

  mixins: [updateValue, getValue],

  props: {
    storeModule: {
      type: String,
      required: true,
    },
  },

  computed: {
    installmentPeriod() {
      const installmentPeriod = this.getValue({
        storeModule: this.storeModule,
        key: 'installment_period',
      });

      if (installmentPeriod === 'None') return '';
      return installmentPeriod.toLowerCase();
    },

    feeAmount() {
      let amount = this.getValue({
        storeModule: this.storeModule,
        key: 'amount',
      });

      if (!isValidDonationAmount(amount)) {
        return false;
      }

      if (amount.charAt(0) === '$') {
        amount = amount.substring(1);
      }

      amount = parseFloat(amount.trim());

      // https://support.stripe.com/questions/passing-the-stripe-fee-on-to-customers
      const feeRate = this.installmentPeriod ? 0.027 : 0.022
      const total = (amount + 0.3) / (1 - feeRate);
      // Fee rounded to two decimal places.
      const fee = Math.round((total - amount) * 100) / 100;

      return `$${fee.toFixed(2)}`;
    },

    isChecked() {
      const payFeesValue = this.getValue({
        storeModule: this.storeModule,
        key: 'pay_fees_value',
      });

      return payFeesValue === 'True';
    },
  },

  methods: {
    onChange(checked) {
      this.updateValue({
        storeModule: this.storeModule,
        key: 'pay_fees_value',
        value: checked ? 'True' : 'False',
      });
    },
  },
};
</script>
