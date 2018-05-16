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
      this.$emit('setValue', { key: 'showCardErrors', value: true });
      this.$emit('setValue', { key: 'showNativeErrors', value: false });
      Vue.nextTick(() => { if (this.valid) this.$emit('onSubmit'); });
    },
  },
};
</script>
