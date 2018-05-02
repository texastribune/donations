<template>
  <fieldset>
    <input
      type="checkbox"
      @input="onInput"
    >
    <span>${{ fee }}</span>
  </fieldset>
</template>

<script>
export default {
  name: 'PayFees',

  props: {
    payFeesValueStoreModule: {
      type: String,
      required: true,
    },

    amountStoreModule: {
      type: String,
      required: true,
    },
  },

  computed: {
    fee() {
      const getter = this.$store.getters[`${this.amountStoreModule}/valueByKey`];
      const amount = parseFloat(getter('amount'));

      if (Number.isNaN(amount) || !amount) return '';

      const total = (amount + 0.30) / (1 - 0.022);
      const fee = Math.floor((total - amount) * 100) / 100;

      return fee.toFixed(2);
    },
  },

  methods: {
    onInput(event) {
      const { checked } = event.target;
      const payFeesVal = checked ? 'True' : 'False';

      this.$store.dispatch(
        `${this.payFeesValueStoreModule}/updateValue`,
        { key: 'pay_fees_value', value: payFeesVal },
      );
    },
  },
};
</script>
