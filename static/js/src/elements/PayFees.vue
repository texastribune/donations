<template>
  <div
    aria-live="polite"
  >
    <div
      :class="classes"
    >
      <input v-if="payFeesState == 'True'"
        id="pay-fees"
        type="checkbox"
        checked=""
        @change="onChange($event.target.checked)"
      >
      <input v-else
        id="pay-fees"
        type="checkbox"
        @change="onChange($event.target.checked)"
      >

      <label
        for="pay-fees"
      >
        I agree to pay
        <span
          v-if="fee"
        >
          {{ fee }}
        </span>
        <span>{{ installmentPeriod }}</span>
        for processing fees. This directs more money to our mission.
      </label>
    </div>
  </div>
</template>

<script>
import validate from 'validate.js';

import updateStoreValue from './mixins/updateStoreValue';
import getStoreValue from './mixins/getStoreValue';

export default {
  name: 'PayFees',

  mixins: [
    updateStoreValue,
    getStoreValue,
  ],

  props: {
    amountStoreModule: {
      type: String,
      required: true,
    },

    installmentPeriodStoreModule: {
      type: String,
      required: true,
    },

    payFeesValueStoreModule: {
      type: String,
      required: true,
    },
  },

  computed: {
    fee() {
      let amount = this.getStoreValue({
        storeModule: this.amountStoreModule,
        key: 'amount',
      });

      if (!this.isValidAmount(amount)) return false;

      amount = parseFloat(amount);

      const total = (amount + 0.30) / (1 - 0.022);
      const fee = Math.floor((total - amount) * 100) / 100;

      return `$${fee.toFixed(2)}`;
    },

    installmentPeriod() {
      const installmentPeriod = this.getStoreValue({
        storeModule: this.installmentPeriodStoreModule,
        key: 'installment_period',
      });

      if (installmentPeriod === 'None') return '';
      return installmentPeriod.toLowerCase();
    },

    payFeesState() {
      const payFeesCheckState = this.getStoreValue({
      storeModule: this.payFeesValueStoreModule,
      key: 'pay_fees_value',
    });
    return payFeesCheckState;
    },

  },

  methods: {
    onChange(checked) {
      this.updateStoreValue({
        storeModule: this.payFeesValueStoreModule,
        key: 'pay_fees_value',
        value: checked ? 'True' : 'False',
      });
    },

    isValidAmount(amount) {
      const isValid = validate(
        { value: amount },
        { value: { numericality: { greaterThanOrEqualTo: 1 } } },
      );
      return typeof isValid === 'undefined';
    },
  },
};
</script>
