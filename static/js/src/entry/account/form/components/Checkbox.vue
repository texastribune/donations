<template>
  <div class="c-checkbox">
    <div class="c-checkbox__inputs" :class="{ 'has-xxxs-btm-marg': hasErrors }">
      <div class="c-checkbox__box">
        <input :id="name" :checked="value" type="checkbox" @change="onChange" />
      </div>
      <div class="c-checkbox__label">
        <label :for="name" class="t-size-s t-lh-b has-text-gray-dark">
          {{ label }}
        </label>
      </div>
    </div>

    <div v-show="hasErrors"><errors :error-messages="errorMessages" /></div>
  </div>
</template>

<script>
import formElementMixin from '../mixins/element';

import Errors from './Errors.vue';

export default {
  name: 'Checkbox',

  components: { Errors },

  mixins: [formElementMixin],

  props: {
    value: {
      type: Boolean,
      required: true,
    },
  },

  methods: {
    onChange(event) {
      this.$emit('input', event.target.checked);
    },
  },
};
</script>
