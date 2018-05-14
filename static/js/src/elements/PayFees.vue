<template>
  <div
    :class="getCssClasses('div')"
  >
    <input
      id="pay-fees"
      :class="getCssClasses('input')"
      type="checkbox"
      @input="onInput($event.target.checked)"
    >
    <label
      :class="getCssClasses('para')"
      for="pay-fees"
    >
      I agree to pay
      <span
        :class="getCssClasses('span')"
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

    inputCssClasses: {
      type: [String, Array],
      default: '',
    },

    spanCssClasses: {
      type: [String, Array],
      default: '',
    },

    paraCssClasses: {
      type: [String, Array],
      default: '',
    },

    divCssClasses: {
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
