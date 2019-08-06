<template>
  <div>
    <label :for="name">
      <input :id="name" :checked="value" type="checkbox" @change="onChange" />
      {{ label }}
    </label>
  </div>
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
