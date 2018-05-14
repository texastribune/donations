<template>
  <ul
    :class="getCssClasses('ul')"
  >
    <li
      v-for="(option, index) in options"
      :key="option.id"
      :class="getCssClasses('li', option)"
    >
      <input
        :value="option.value"
        :name="name"
        :checked="value === option.value"
        :id="getLabelConnector(index)"
        class="hidden"
        type="radio"
        @input="updateSingleValue($event.target.value)"
      >
      <label
        :for="getLabelConnector(index)"
        :class="getCssClasses('label', option)"
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

    ulCssClasses: {
      type: String,
      default: '',
    },
  },

  methods: {
    getLabelConnector(index) {
      return `${this.name}-${index}`;
    },
  },
};
</script>
