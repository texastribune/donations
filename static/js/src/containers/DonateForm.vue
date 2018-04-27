<template>
  <form
    action="/charge"
    method="post"
  >
    <amount identifier="amount" />
  </form>
</template>

<script>
import Amount from '../containers/Amount.vue';

export default {
  name: 'DonateForm',

  components: {
    Amount,
  },
};
</script>
