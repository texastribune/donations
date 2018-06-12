<template>
  <ul
    :class="classes"
  >
    <li
      v-for="(option, index) in options"
      :key="option.id"
    >
      <input
        :aria-labelledby="ariaLabelledby"
        :aria-describedby="ariaDescribedby"
        :value="option.value"
        :name="name"
        :checked="value === option.value"
        :id="getConnector(index)"
        type="radio"
        @input="updateSingleValue($event.target.value)"
      >
      <label
        :for="getConnector(index)"
      >
        {{ option.text }}
      </label>
    </li>
  </ul>
</template>

<script>
import connectedElement from './mixins/connectedElement';
import labelConnector from './mixins/labelConnector';
import aria from './mixins/aria';

export default {
  name: 'Frequency',

  mixins: [
    aria,
    labelConnector,
    connectedElement,
  ],

  props: {
    options: {
      type: Array,
      required: true,
    },
  },

  methods: {
    getConnector(index) {
      return `_${this.randConnector}-${index}`;
    },
  },
};
</script>
