<template>
  <div :class="classesWithValidation">
    <label v-if="hasLabel" :for="connector">{{ labelText }}</label>
    <div :class="{ 'c-freq' : showFrequency }">
      <input
        :id="connector"
        :aria-label="ariaLabel"
        :aria-invalid="!isValid ? true : false"
        :aria-required="required"
        :value="value"
        :name="name"
        :placeholder="placeholder"
        :type="type"
        :inputmode="inputmode"
        @input="updateSingleValue($event.target.value)"
      />
      <div v-if="showFrequency" class="c-freq__label">
        <frequency-display :store-module="storeModule" />
      </div>
    </div>
    <p v-if="showError && !isValid" role="alert">{{ message }}</p>
  </div>
</template>

<script>
import connectedElement from './mixins/connected-element';
import labelConnector from './mixins/label-connector';
import FrequencyDisplay from './FrequencyDisplay.vue';

export default {
  name: 'TextInput',

  components: {
    FrequencyDisplay,
  },

  mixins: [connectedElement, labelConnector],

  props: {
    hasLabel: {
      type: Boolean,
      default: true,
    },

    labelText: {
      type: String,
      required: true,
    },

    placeholder: {
      type: String,
      default: '',
    },

    required: {
      type: Boolean,
      default: true,
    },

    type: {
      type: String,
      default: 'text',
    },

    inputmode: {
      type: String,
      default: null,
      required: false,
    },

    showFrequency: {
      type: Boolean,
      default: false,
      required: false,
    },
  },

  computed: {
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
      if (!this.showError || this.isValid) return classes;
      return `invalid ${classes}`;
    },
  },
};
</script>
