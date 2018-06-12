<template>
  <ul
    :class="classes"
  >
    <li
      v-for="(option, index) in options"
      :key="option.id"
    >
      <input
        :value="option.value"
        :name="name"
        :checked="value === option.value"
        :id="getLabelConnector(option, index)"
        type="radio"
        @input="updateSingleValue($event.target.value)"
      >
      <label
        :for="getLabelConnector(option, index)"
      >
        {{ option.text }}
      </label>
    </li>
  </ul>
</template>

<script>
import connectedElement from './mixins/connectedElement';

export default {
  name: 'Frequency',

  mixins: [connectedElement],

  props: {
    options: {
      type: Array,
      required: true,
    },
  },

  methods: {
    getLabelConnector({ connector }, index) {
      if (connector) return `${connector}-${index}`;
      return `${this.name}-${index}`;
    },
  },
};
</script>
