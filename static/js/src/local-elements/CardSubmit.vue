<template>
  <input
    :class="getCssClasses()"
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
  },

  methods: {
    onClick() {
      this.$emit('onSubmit');
    },
  },
};
</script>
