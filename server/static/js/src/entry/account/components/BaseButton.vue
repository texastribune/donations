<template>
  <button
    type="button"
    class="c-button"
    :class="classes"
    :disabled="disabled"
    @click="onClick"
  >
    {{ text }}
  </button>
</template>

<script>
export default {
  name: 'BaseButton',

  props: {
    disabled: {
      type: Boolean,
      default: false,
    },

    text: {
      type: String,
      required: true,
    },

    display: {
      type: Object,
      default: () => ({}),
    },

    extraClasses: {
      type: Array,
      default: () => [],
    },
  },

  computed: {
    classes() {
      const classes = [];
      const merged = {
        isFullWidth: true,
        size: '',
        bg: 'teal',
        color: 'white',
        ...this.display,
      };
      const { isFullWidth, size, bg, color } = merged;

      if (isFullWidth) {
        classes.push('l-width-full');
        classes.push('l-display-block');
      }

      if (size) classes.push(`c-button--${size}`);

      classes.push(`has-bg-${bg}`);
      classes.push(`has-text-${color}`);

      return [...classes, ...this.extraClasses].join(' ');
    },
  },

  methods: {
    onClick() {
      this.$emit('onClick');
    },
  },
};
</script>
