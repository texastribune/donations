<template>
  <input
    :disabled="!token"
    :value="value"
    type="submit"
    @click="onClick"
  >
</template>

<script>
export default {
  name: 'CardSubmit',

  props: {
    value: {
      type: String,
      default: 'Submit',
    },

    token: {
      type: String,
      required: true,
    },
  },

  methods: {
    onClick() {
      this.$emit('onSubmit');
    },
  },
};
</script>
