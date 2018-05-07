<template>
  <ul
    :class="ulClass"
  >
    <li
      v-for="(option, index) in options"
      :key="option.id"
      :class="getClasses(option, 'li')"
    >
      <input
        :value="option.value"
        :name="name"
        :checked="value === option.value"
        :id="getLabelConnector(index)"
        class="hidden"
        type="radio"
        @input="onInput($event.target.value)"
      >
      <label
        :for="getLabelConnector(index)"
        :class="getClasses(option, 'label')"
      >
        {{ option.text }}
      </label>
    </li>
  </ul>
</template>

<script>
import mapValueToElement from '../mixins/mapValueToElement';
import replaceSingleValueOnInput from '../mixins/replaceSingleValueOnInput';

export default {
  name: 'Frequency',

  mixins: [
    mapValueToElement,
    replaceSingleValueOnInput,
  ],

  props: {
    options: {
      type: Array,
      required: true,
    },

    ulClass: {
      type: String,
      default: '',
    },
  },

  methods: {
    getLabelConnector(index) {
      return `${this.name}-${index}`;
    },

    getClasses(option, elName) {
      const { [`${elName}Classes`]: classes } = option;

      if (classes) {
        if (typeof classes === 'string') {
          return classes;
        } else if (Array.isArray(classes)) {
          return classes.join(' ');
        }
      }
      return '';
    },
  },
};
</script>
