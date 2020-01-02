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

      const total = (amount + 0.3) / (1 - 0.022);
      const amexTotal = amount / (1 - 0.035);

      const fee = Math.floor((total - amount) * 100) / 100;
      const amexFee = Math.floor((amexTotal - amount) * 100) / 100;

      const lowerFee = Math.min(fee, amexFee);
      const higherFee = Math.max(fee, amexFee);

      if (lowerFee === higherFee) {
        return `$${lowerFee.toFixed(2)}`;
      }

      return `between $${lowerFee.toFixed(2)} and $${higherFee.toFixed(2)}`;
    },

    installmentPeriod() {
      const installmentPeriod = this.getValue({
        storeModule: this.storeModule,
        key: 'installment_period',
      });

      if (installmentPeriod === 'None') return '';
      return installmentPeriod.toLowerCase();
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
