<template>
  <input
    :value="token"
    name="stripeToken"
    type="hidden"
  >
</template>

<script>
export default {
  name: 'Token',

  props: {
    token: {
      type: String,
      required: true,
    },
  },
};
</script>
