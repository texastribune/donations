<template>
  <form class="c-mini-form" @submit.prevent="$emit('onSubmit', currentFields)">
    <validation-provider
      v-slot="{ errors, flags }"
      :name="name"
      :rules="currentFields[name].rules"
      immediate
      slim
    >
      <div class="c-mini-form__input">
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
      </div>
    </validation-provider>
    <div class="c-mini-form__submit">
      <submit :disabled="!formIsValid" :value="submitText" />
    </div>
  </form>
</template>

<script>
import formMixin from '../mixins';

export default {
  name: 'TextInputAndSubmit',

  mixins: [formMixin],

  props: {
    submitText: {
      type: String,
      default: 'Submit',
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
