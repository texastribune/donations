<template>
  <input
    :class="classes"
    :value="value"
    type="submit"
    @click="onClick"
  >
</template>

<script>
import Vue from 'vue';

export default {
  name: 'ManualSubmit',

  props: {
    value: {
      type: String,
      default: 'Submit',
    },

    formIsValid: {
      type: Boolean,
      required: true,
    },
  },

  methods: {
    onClick() {
      this.$emit('setValue', { key: 'showManualErrors', value: true });
      this.$emit('setValue', { key: 'showNativeErrors', value: false });
      if (this.formIsValid) Vue.nextTick(() => { this.$emit('onSubmit'); });
    },
  },
};
</script>
