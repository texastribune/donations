<template>
  <fieldset>
    <input
      type="checkbox"
      @input="onInput($event.target.checked)"
    >
    <span>{{ fee }}</span>
  </fieldset>
</template>

<script>
import updateCallbackOnly from '../mixins/updateCallbackOnly';

export default {
  name: 'PayFees',

  mixins: [updateCallbackOnly],

  props: {
    amountStoreModule: {
      type: String,
      required: true,
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
