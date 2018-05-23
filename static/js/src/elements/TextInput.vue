<template>
  <div>
    <label
      v-if="hasLabel"
      :for="connector"
    >
      {{ labelText }}
    </label>
    <input
      :id="connector"
      :aria-label="ariaLabel"
      :value="value"
      :name="name"
      :placeholder="placeholder"
      :class="classes"
      :type="type"
      @input="updateSingleValue($event.target.value)"
    >
    <p
      v-if="showError && !valid"
    >
      {{ errorMessage }}
    </p>
  </div>
</template>

<script>
import connectedElement from './mixins/connectedElement';

export default {
  name: 'TextInput',

  mixins: [connectedElement],

  props: {
    maxlength: {
      type: [String, Boolean],
      default: false,
    },

    placeholder: {
      type: String,
      default: '',
    },

    type: {
      type: String,
      default: 'text',
    },
  },
};
</script>
