<template>
  <input
    type="submit"
    class="c-button c-button--s has-text-white has-bg-teal l-width-full l-display-block"
    :value="value"
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
  },
};
</script>
