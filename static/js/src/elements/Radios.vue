<template>
  <ul
    :class="getClasses({ elName: 'list' })"
  >
    <li
      v-for="(option, index) in options"
      :key="option.id"
      :class="getClasses({ elName: 'li', obj: option })"
    >
      <input
        :value="option.value"
        :name="name"
        :checked="value === option.value"
        :id="getLabelConnector(index)"
        :class="getClasses({ elName: 'input', obj: option })"
        type="radio"
        @input="updateSingleValue($event.target.value)"
      >
      <label
        :for="getLabelConnector(index)"
        :class="getClasses({ elName: 'label', obj: option })"
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

    listClasses: {
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
