<template>
  <label
    :for="name"
    class="c-checkbox t-size-s has-text-gray-dark l-display-block"
  >
    <input :id="name" :checked="value" type="checkbox" @change="onChange" />
    {{ label }}
  </label>
</template>

<script>
import formElementMixin from '../mixins/form-element';

export default {
  name: 'Checkbox',

  mixins: [formElementMixin],

  props: {
    value: {
      type: Boolean,
      required: true,
    },
  },

  methods: {
    onChange(event) {
      this.$emit('input', event.target.checked);
    },
  },
};
</script>
