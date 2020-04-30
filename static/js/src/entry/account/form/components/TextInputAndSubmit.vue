<template>
  <validation-observer v-slot="{ handleSubmit }">
    <form
      :key="formKey"
      class="c-mini-form"
      @submit.prevent="handleSubmit(onSubmit)"
    >
      <validation-provider
        v-slot="{ errors, pristine, changed, valid }"
        :rules="rules"
        :name="name"
        slim
      >
        <div class="c-mini-form__input">
          <text-input
            v-model="inputModel"
            :label="label"
            :name="name"
            :prevent-paste="preventPaste"
            :read-only="readOnly"
            :show-label="false"
            :error-messages="errors"
            :pristine="pristine"
            :changed="changed"
            :valid="valid"
            @updateFlags="updateFlags"
          />
        </div>
      </validation-provider>

      <div class="c-mini-form__submit"><submit :value="submitText" /></div>
    </form>
  </validation-observer>
</template>

<script>
import formMixin from '../mixins/form';

export default {
  name: 'TextInputAndSubmit',

  mixins: [formMixin],

  props: {
    name: {
      type: String,
      required: true,
    },

    label: {
      type: String,
      required: true,
    },

    rules: {
      type: String,
      required: true,
    },

    preventPaste: {
      type: Boolean,
      default: false,
    },

    readOnly: {
      type: Boolean,
      default: false,
    },

    submitText: {
      type: String,
      default: 'Submit',
    },
  },

  computed: {
    inputModel: {
      get() {
        const [firstKey] = Object.keys(this.currentFields);

        return this.currentFields[firstKey].value;
      },

      set(value) {
        const [firstKey] = Object.keys(this.currentFields);

        this.currentFields[firstKey].value = value;
      },
    },
  },
};
</script>
