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

    <select
      :aria-labelledby="ariaLabelledby"
      :aria-describedby="ariaDescribedby"
      :aria-label="ariaLabel"
      :aria-required="required"
      @change="onChange($event.target.selectedIndex)">
      <option
        v-for="(item, index) in listOfChoices"
        :selected="item.value == isSelected"
        :id="index"
        :key="index"
        :value="item.value">
        {{ item.text }}
      </option>
    </select>
  </div>
</template>

<script>
import aria from './mixins/aria';
import labelConnector from './mixins/labelConnector';
import updateStoreValue from './mixins/updateStoreValue';
import getStoreValue from './mixins/getStoreValue';

export default {
  name: 'SelectList',
  mixins: [
    aria,
    labelConnector,
    updateStoreValue,
    getStoreValue,
  ],
  props: {
    name: {
      type: String,
      required: true,
    },
    listOfChoices: {
      type: Array,
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
    selectListStoreModule: {
      type: String,
      required: true,
    },

  },
  computed: {
    isSelected() {
      let selectList = this.getStoreValue({
        storeModule: this.selectListStoreModule,
        key: this.name,
      });
      return selectList;
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
    onChange(selectedIndex) {
      this.updateStoreValue({
        storeModule: this.selectListStoreModule,
        key: this.name,
        value: this.listOfChoices[selectedIndex].value,
      });
    },
  },
};
</script>
