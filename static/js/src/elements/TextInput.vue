<template>
  <div>
    <input
      :value="value"
      :name="name"
      :maxlength="maxlength"
      :placeholder="placeholder"
      :class="classes"
      type="text"
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
    placeholder: {
      type: String,
      default: '',
    },

    maxlength: {
      type: [String, Boolean],
      default: false,
    },
  },
};
</script>
