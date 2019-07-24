<template>
  <button type="button" :disabled="disabled" @click="onClick">
    {{ text }}
  </button>
</template>

<script>
export default {
  name: 'Button',

  props: {
    text: {
      type: String,
      required: true,
    },

    disabled: {
      type: Boolean,
      required: true,
    },
  },

  methods: {
    onClick(e) {
      this.$emit('onClick', e.target.value);
    },
  },
};
</script>
