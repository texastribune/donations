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
        :read-only="readOnly"
        @updateFlags="updateFlags"
      />
    </validation-provider>
    <submit :disabled="!formIsValid" :value="submitText" />
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

    submitText: {
      type: String,
      default: 'Save',
    },

    readOnly: {
      type: Boolean,
      default: false,
    },

    showErrorImmediately: {
      type: Boolean,
      default: true,
    },
  },
};
</script>
