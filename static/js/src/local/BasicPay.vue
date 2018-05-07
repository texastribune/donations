<template>
  <div>
    <card
      stripe="pk_test_sSUhBbATSHteQVZZvz6R5aYe"
      @change="complete = $event.complete"
    />
    <button
      :disabled="!complete"
      @click="pay"
    >
      Donate
    </button>
  </div>
</template>

<script>
import { Card, createToken } from 'vue-stripe-elements-plus';

export default {
  name: 'BasicPay',

  components: {
    Card,
  },

  data() {
    return { complete: false };
  },

  methods: {
    pay() {
      createToken().then(({ token: { id } }) => {
        this.$emit('setToken', id);
        // this.$parent.$refs.form.submit();
      }).catch(() => {
        window.location.href = '/error';
      });
    },
  },
};
</script>
