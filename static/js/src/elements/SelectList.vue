<template>
  <div
    :class="classes"
  >
    <label
      v-if="hasLabel"
      :for="connector"
    >
      {{ labelText }}
    </label>

    <input
      id="select-list"
      :selected="isSelected"
      type="select"
      @change="onChange($event.target.selected)"
    >

    <select
      :aria-labelledby="ariaLabelledby"
      :aria-describedby="ariaDescribedby"
      :aria-label="ariaLabel"
      :aria-required="required"
      :class="classes">
      <option
        v-for="(option, index) in options.list"
        :selected="index == options.default"
        :id="getConnector(index)"
        :key="option.value"
        :value="option.value" >
        {{ option.text }}
      </option>
    </select>
  </div>
</template>

<script>
import connectedElement from './mixins/connectedElement';
import labelConnector from './mixins/labelConnector';
import aria from './mixins/aria';

export default {
  name: 'SelectList',
  mixins: [
    aria,
    connectedElement,
    labelConnector,
  ],
  props: {
    options: {
      type: Object,
      required: true,
    },
    hasLabel: {
      type: Boolean,
      default: true,
    },
    labelText: {
      type: String,
      required: true,
    },
    required: {
      type: Boolean,
      default: true,
    },
    type: {
      type: String,
      default: 'select',
    },
    selectGeoStateValueStoreModule: {
      type: String,
      required: true,
    },
  },
  computed: {
    isSelected() {
      const payFeesValue = this.getStoreValue({
        storeModule: this.selectGeoStateValueStoreModule,
        key: 'shipping_state',
      });
    },
    onChange(selected) {
      console.log(`onChange: ${selected}`);
      this.updateStoreValue({
        storeModule: this.selectGeoStateValueStoreModule,
        key: 'shipping_state',
        value: selected,
      });
    },
    connector() {
      if (!this.hasLabel) return false;
      return `_${this.randConnector}`;
    },
    ariaLabel() {
      if (this.hasLabel) return false;
      return this.labelText;
    },
    classesWithValidation() {
      const { classes } = this;
      return classes;
    },
  },
  methods: {
    getConnector(index) {
      return `_${this.randConnector}-${index}`;
    },
  },
};
</script>
