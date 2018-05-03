<template>
  <fieldset>
    <input
      v-for="option in options"
      :key="option.id"
      :value="option.value"
      :name="name"
      :checked="value === option.value"
      type="radio"
      @input="onInput($event.target.value)"
    >
  </fieldset>
</template>

<script>
import connectedElement from '../mixins/connectedElement';
import updateSingleValue from '../mixins/updateSingleValue';

export default {
  name: 'Frequency',

  mixins: [
    connectedElement,
    updateSingleValue,
  ],

  props: {
    onUpdate: {
      type: Function,
      default: null,
    },

    options: {
      type: Array,
      required: true,
    },
  },

  methods: {
    onInput(newValue) {
      this.updateSingleValue(newValue);
      if (this.onUpdate) this.onUpdate(newValue);
    },
  },
};
</script>
