<template>
  <fieldset>
    <input
      v-for="option in options"
      :key="option.id"
      :value="option.value"
      :name="identifier"
      :checked="value === option.value"
      type="radio"
      @input="updateValue($event.target.value)"
    >
  </fieldset>
</template>

<script>
import connectedFormElement from '../mixins/connectedFormElement';

export default {
  name: 'Frequency',

  mixins: [connectedFormElement],

  data() {
    return {
      options: [
        { id: 0, text: 'monthly', value: 'monthly' },
        { id: 1, text: 'yearly', value: 'yearly' },
        { id: 2, text: 'one time', value: 'None' },
      ],
    };
  },
};
</script>
