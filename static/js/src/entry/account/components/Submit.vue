<template>
  <input type="submit" :value="value" :disabled="disabled" />
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
