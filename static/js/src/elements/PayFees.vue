<template>
  <div
    aria-live="polite"
  >
    <div
      v-if="fee"
      :class="classes"
    >
      <input
        id="pay-fees"
        type="checkbox"
        @change="onChange($event.target.checked)"
      >
      <label
        for="pay-fees"
      >
        I agree to pay
        <span>{{ fee }}</span>
        for processing fees. Paying fees directs more money to our mission.
      </label>
    </div>
  </div>
</template>

<script>
import validate from 'validate.js';

import updateStoreValue from './mixins/updateStoreValue';

export default {
  name: 'PayFees',

  mixins: [updateStoreValue],

  props: {
    amountStoreModule: {
      type: String,
      required: true,
    },

    payFeesValueStoreModule: {
      type: String,
      required: true,
    },

    containerClasses: {
      type: [String, Array],
      default: '',
    },
  },

  computed: {
    fee() {
      const getter =
        this.$store.getters[`${this.amountStoreModule}/valueByKey`];
      let amount = getter('amount');

      if (!this.isValidAmount(amount)) return false;

      amount = parseFloat(amount.trim());

      const total = (amount + 0.30) / (1 - 0.022);
      const fee = Math.floor((total - amount) * 100) / 100;

      return `$${fee.toFixed(2)}`;
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
        { value: amount.trim() },
        { value: { numericality: { greaterThanOrEqualTo: 1 } } },
      );
      return typeof isValid === 'undefined';
    },
  },
};
</script>
