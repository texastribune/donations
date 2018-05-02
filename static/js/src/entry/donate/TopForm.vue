<template>
  <form
    action="/charge"
    method="post"
  >
    <amount
      identifier="amount"
      store-module="baseForm"
    />

    <frequency
      identifier="installment_period"
      store-module="baseForm"
    />

    <open-ended
      identifier="openended_status"
      store-module="baseForm"
    />
  </form>
</template>

<script>
import Amount from '../../elements/Amount.vue';
import Frequency from '../../elements/Frequency.vue';
import OpenEnded from '../../elements/OpenEnded.vue';

export default {
  name: 'TopForm',

  components: {
    Amount,
    Frequency,
    OpenEnded,
  },
};
</script>
