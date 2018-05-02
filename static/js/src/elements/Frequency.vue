<template>
  <fieldset>
    <input
      v-for="option in options"
      :key="option.id"
      :value="option.value"
      :name="identifier"
      :checked="value === option.value"
      type="radio"
      @input="onInput($event.target.value)"
    >
  </fieldset>
</template>

<script>
import connectedFormElement from '../mixins/connectedFormElement';

export default {
  name: 'Frequency',

  mixins: [connectedFormElement],

  props: {
    openEndedStoreModule: {
      type: String,
      required: true,
    },
  },

  data() {
    return {
      options: [
        { id: 0, text: 'monthly', value: 'monthly' },
        { id: 1, text: 'yearly', value: 'yearly' },
        { id: 2, text: 'one time', value: 'None' },
      ],
    };
  },

  methods: {
    onInput(newValue) {
      this.updateValue(newValue);
      this.updateOpenEnded();
    },

    updateOpenEnded() {
      const { value: freqValue } = this;
      let openEndedVal;

      if (freqValue === 'yearly' || freqValue === 'monthly') {
        openEndedVal = 'Open';
      } else if (freqValue === 'None') {
        openEndedVal = 'None';
      }

      this.$store.dispatch(
        `${this.openEndedStoreModule}/updateValue`,
        { key: 'openended_status', value: openEndedVal },
      );
    },
  },
};
</script>
