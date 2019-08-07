<template>
  <input
    type="submit"
    class="c-button c-button--s has-text-white has-bg-teal l-width-full l-display-block"
    :value="value"
    :disabled="disabled"
  />
</template>

<script>
export default {
  name: 'Submit',

  props: {
    value: {
      type: String,
      default: 'Submit',
    },

    disabled: {
      type: Boolean,
      required: true,
    },
  },
};
</script>
