<template>
  <fieldset>
    <input
      :class="getClasses('input', this)"
      type="checkbox"
      @input="onInput($event.target.checked)"
    >
    <p
      :class="getClasses('para', this)"
    >
      <span
        :class="getClasses('span', this)"
      >
        {{ fee }}
      </span>
    </p>
  </fieldset>
</template>

<script>
import updateCallbackOnly from '../mixins/updateCallbackOnly';
import iterativeCssClasses from '../mixins/iterativeCssClasses';

export default {
  name: 'PayFees',

  mixins: [
    iterativeCssClasses,
    updateCallbackOnly,
  ],

  props: {
    amountStoreModule: {
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
  },

  computed: {
    fee() {
      const getter =
        this.$store.getters[`${this.amountStoreModule}/valueByKey`];
      const amount = parseFloat(getter('amount'));

      if (Number.isNaN(amount) || !amount) return '';

      const total = (amount + 0.30) / (1 - 0.022);
      const fee = Math.floor((total - amount) * 100) / 100;

      return `$${fee.toFixed(2)}`;
    },
  },
};
</script>
