<template>
  <form @submit.prevent="$emit('onSubmit', currentFields)">
    <validation-provider
      v-slot="{ errors, flags }"
      :name="name"
      :rules="rules"
      immediate
    >
      <text-input
        v-model="currentFields[name].value"
        :error-messages="errors"
        :flags="flags"
        :name="name"
        :label="label"
        :show-label="false"
        :show-error-immediately="showErrorImmediately"
        @updateFlags="updateFlags"
      />
    </validation-provider>
    <submit :disabled="!formIsValid" value="Save" />
  </form>
</template>

<script>
import formMixin from '../mixins/form';

export default {
  name: 'TextInputAndButton',

  mixins: [formMixin],

  props: {
    rules: {
      type: Object,
      required: true,
    },

    label: {
      type: String,
      required: true,
    },

    name: {
      type: String,
      required: true,
    },

    showErrorImmediately: {
      type: Boolean,
      default: true,
    },
  },
};
</script>
