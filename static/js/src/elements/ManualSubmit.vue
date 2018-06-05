<template>
  <input
    :class="classes"
    :value="value"
    :disabled="isFetchingToken"
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

    isFetchingToken: {
      type: Boolean,
      required: true,
    },
  },

  methods: {
    onClick() {
      const updates = [
        { key: 'showManualErrors', value: true },
        { key: 'showNativeErrors', value: false },
      ];

      this.$emit('setValue', updates);
      if (this.formIsValid) Vue.nextTick(() => { this.$emit('onSubmit'); });
    },
  },
};
</script>
