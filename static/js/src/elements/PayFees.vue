<template>
  <input
    type="checkbox"
    @input="onInput"
  >
</template>

<script>
export default {
  name: 'PayFees',

  props: {
    payFeesValueStoreModule: {
      type: String,
      required: true,
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
