<template>
  <form
    action="/charge"
    method="post"
  >
    <amount
      identifier="amount"
      store-module="baseForm"
    />
  </form>
</template>

<script>
import Amount from '../../elements/Amount.vue';

export default {
  name: 'TopForm',

  components: {
    Amount,
  },
};
</script>
