<template>
  <input
    :value="value"
    type="text"
    @input="updateValue($event.target.value)"
  >
</template>

<script>
import formStoreOrLocal from '../mixins/formStoreOrLocal';

export default {
  name: 'Amount',

  mixins: [formStoreOrLocal],
};
</script>
