<template>
  <form @submit.prevent="$emit('onSubmit', currentFields)">
    <validation-provider
      v-slot="{ errors, flags }"
      :name="name"
      :rules="currentFields[name].rules"
      immediate
    >
      <text-input
        v-model="currentFields[name].value"
        :name="currentFields[name].name"
        :label="currentFields[name].label"
        :read-only="currentFields[name].readOnly"
        :error-messages="errors"
        :flags="flags"
        :show-label="false"
        :show-error-immediately="false"
        @updateFlags="updateFlags"
      />
    </validation-provider>
    <submit :disabled="!formIsValid" :value="submitText" />
  </form>
</template>

<script>
import formMixin from '../mixins/form';

export default {
  name: 'TextInputAndSubmit',

  mixins: [formMixin],

  props: {
    submitText: {
      type: String,
      default: 'Save',
    },

    readOnly: {
      type: Boolean,
      default: false,
    },
  },

  computed: {
    name() {
      const [onlyFieldKey] = Object.keys(this.initialFields);
      return this.initialFields[onlyFieldKey].name;
    },
  },
};
</script>
