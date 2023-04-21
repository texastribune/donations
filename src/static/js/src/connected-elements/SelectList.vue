<template>
  <div :class="classes">
    <label :for="connector">{{ labelText }}</label>

    <select
      :id="connector"
      :name="name"
      @change="updateSingleValue($event.target.value)"
    >
      <option
        v-for="option in options"
        :key="option.id"
        :value="option.value"
        :selected="value === option.value"
        >{{ option.text }}</option
      >
    </select>
  </div>
</template>

<script>
import connectedElement from './mixins/connected-element';
import labelConnector from './mixins/label-connector';

export default {
  name: 'SelectList',

  mixins: [labelConnector, connectedElement],

  props: {
    options: {
      type: Array,
      required: true,
    },

    labelText: {
      type: String,
      required: true,
    },
  },

  computed: {
    connector() {
      return `_${this.randConnector}`;
    },
  },
};
</script>
