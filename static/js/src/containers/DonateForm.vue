<template>
  <form
    action="/charge"
    method="post"
  >
    <amount
      :param-value="paramAmount"
      use-store
      react-to-param
      identifier="amount"
    />
  </form>
</template>

<script>
import Amount from '../containers/Amount.vue';

export default {
  name: 'DonateForm',

  components: {
    Amount,
  },

  computed: {
    paramAmount() {
      return this.$route.query.amount;
    },
  },
};
</script>
