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

    valid: {
      type: Boolean,
      required: true,
    },
  },

  methods: {
    onClick() {
      this.$emit('toggleError', 'stripeToken', true);
      this.$emit('setValue', 'showErrors', true);
      if (this.valid) this.$emit('onSubmit');
    },
  },
};
</script>
