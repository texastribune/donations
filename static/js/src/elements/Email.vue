<template>
  <div>
    <input
      :value="value"
      :name="name"
      :placeholder="placeholder"
      :class="classes"
      type="email"
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
  name: 'Email',

  mixins: [connectedElement],

  props: {
    placeholder: {
      type: String,
      default: '',
    },
  },
};
</script>
