<template>
  <ul :class="classes">
    <li v-for="(option, index) in options" :key="option.id">
      <input
        :id="getConnector(index)"
        :value="option.value"
        :name="name"
        :checked="value === option.value"
        type="radio"
        @change="updateSingleValue($event.target.value)"
      />
      <label :for="getConnector(index)">{{ option.text }}</label>
    </li>
  </ul>
</template>

<script>
import connectedElement from './mixins/connected-element';
import labelConnector from './mixins/label-connector';

export default {
  name: 'Frequency',

  mixins: [labelConnector, connectedElement],

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
