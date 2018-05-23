<template>
  <div
    :class="getClasses({ elName: 'container' })"
  >
    <input
      id="pay-fees"
      :class="getClasses({ elName: 'checkbox' })"
      type="checkbox"
      @input="onInput($event.target.checked)"
    >
    <label
      :class="getClasses({ elName: 'text' })"
      for="pay-fees"
    >
      I agree to pay
      <span
        :class="getClasses({ elName: 'fee' })"
      >
        {{ fee }}
      </span>
      for processing fees. Paying fees directs more money to our mission.
    </label>
  </div>
</template>

<script>
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

    checkboxClasses: {
      type: [String, Array],
      default: '',
    },

    feeClasses: {
      type: [String, Array],
      default: '',
    },

    textClasses: {
      type: [String, Array],
      default: '',
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
      const amount = parseFloat(getter('amount').trim());

      const total = (amount + 0.30) / (1 - 0.022);
      const fee = Math.floor((total - amount) * 100) / 100;

      return `$${fee.toFixed(2)}`;
    },
  },

  methods: {
    onInput(checked) {
      this.updateStoreValue({
        storeModule: this.payFeesValueStoreModule,
        key: 'pay_fees_value',
        value: checked ? 'True' : 'False',
      });
    },
  },
};
</script>
