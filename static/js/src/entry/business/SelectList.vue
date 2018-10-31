<template>
  <div
    :class="classes"
  >
    <label for="state-select-list">
      {{ labelText }}
    </label>

    <select
      id="state-select-list"
      :aria-labelledby="ariaLabelledby"
      :aria-describedby="ariaDescribedby"
      @change="onChange($event.target.selectedIndex)">
      <option
        v-for="(item, index) in listOfChoices"
        :selected="item.value == isSelected"
        :id="index"
        :key="index+'_'+item.value"
        :value="item.value">
        {{ item.text }}
      </option>
    </select>
  </div>
</template>

<script>
import aria from '../../elements/mixins/aria';
import labelConnector from '../../elements/mixins/labelConnector';
import updateStoreValue from '../../elements/mixins/updateStoreValue';
import getStoreValue from '../../elements/mixins/getStoreValue';

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
