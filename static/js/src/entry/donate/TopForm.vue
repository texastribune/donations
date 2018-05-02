<template>
  <form
    action="/charge"
    method="post"
  >
    <text-input
      name="amount"
      store-module="baseForm"
    />

    <frequency
      name="installment_period"
      store-module="baseForm"
      open-ended-store-module="baseForm"
    />

    <hidden-input
      name="openended_status"
      store-module="baseForm"
    />

    <pay-fees
      store-module="baseForm"
      pay-fees-value-store-module="baseForm"
      amount-store-module="baseForm"
    />

    <hidden-input
      name="pay_fees_value"
      store-module="baseForm"
    />

    <level
      amount-store-module="baseForm"
      installment-period-store-module="baseForm"
    />
  </form>
</template>

<script>
import HiddenInput from '../../elements/HiddenInput.vue';
import Frequency from '../../elements/Frequency.vue';
import Level from '../../elements/Level.vue';
import PayFees from '../../elements/PayFees.vue';
import TextInput from '../../elements/TextInput.vue';

export default {
  name: 'TopForm',

  components: {
    HiddenInput,
    TextInput,
    Frequency,
    PayFees,
    Level,
  },
};
</script>
