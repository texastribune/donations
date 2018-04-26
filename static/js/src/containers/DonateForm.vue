<template>
  <form
    action="/charge"
    method="post"
  >
    <amount
      :param-amount="paramAmount"
      use-store
      use-query-param
    />
  </form>
</template>

<script>
import Amount from '../components/Amount.vue';

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
