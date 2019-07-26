<template>
  <validation-observer
    tag="form"
    @submit.prevent="$emit('onSubmit', currentFields)"
  >
    <validation-provider
      v-slot="{ errors, flags }"
      name="firstName"
      :rules="{ required: true }"
      immediate
    >
      <text-input
        v-model="currentFields.firstName.value"
        :error-messages="errors"
        :flags="flags"
        label="First name"
        name="firstName"
        @addFlags="addFlags"
      />
    </validation-provider>
    <validation-provider
      v-slot="{ errors, flags }"
      name="lastName"
      :rules="{ required: true }"
      immediate
    >
      <text-input
        v-model="currentFields.lastName.value"
        :error-messages="errors"
        :flags="flags"
        label="Last name"
        name="lastName"
        @addFlags="addFlags"
      />
    </validation-provider>
    <validation-provider
      v-slot="{ errors, flags }"
      name="email"
      :rules="{ required: true, email: true }"
      immediate
    >
      <text-input
        v-model="currentFields.email.value"
        :error-messages="errors"
        :flags="flags"
        label="Email"
        name="email"
        @addFlags="addFlags"
      >
        <p v-show="showEmailConfirmation" class="has-text-error">
          <strong>Are you sure?</strong> Changing this will log you out of your
          account, and you won't be able to log back in with
          <strong>Foobar</strong>. Changing your account email will not affect
          your email subscriptions.
        </p>
        <p v-show="!showEmailConfirmation">
          Notice: This email is for logging into your account. Changing it will
          not affect your email newsletters.
        </p>
      </text-input>
    </validation-provider>
    <validation-provider
      v-if="showEmailConfirmation"
      v-slot="{ errors, flags }"
      name="confirmedEmail"
      :rules="{ required: true, is: currentFields.email.value }"
      immediate
    >
      <text-input
        v-model="currentFields.confirmedEmail.value"
        :error-messages="errors"
        :flags="flags"
        label="Type your email again to confirm the change"
        name="confirmedEmail"
        prevent-paste
        @addFlags="addFlags"
      />
    </validation-provider>
    <validation-provider
      v-slot="{ errors, flags }"
      name="zip"
      :rules="{ required: true, numeric: true }"
      immediate
    >
      <text-input
        v-model="currentFields.zip.value"
        :error-messages="errors"
        :flags="flags"
        label="ZIP code"
        name="zip"
        @addFlags="addFlags"
      />
    </validation-provider>
    <div>
      <label for="marketing">News & Offers</label>
      <label for="marketing">
        <input
          id="marketing"
          v-model="currentFields.marketing.value"
          type="checkbox"
          name="marketing"
        />
        Yes, I would like to receive emails with special promotions, product
        announcements and membership opportunities.
      </label>
    </div>
    <submit :disabled="!isValid" />
  </validation-observer>
</template>

<script>
import { ValidationObserver, ValidationProvider } from 'vee-validate';

import TextInput from '../../../components/TextInput.vue';
import Submit from '../../../components/Submit.vue';

export default {
  name: 'EditContactInfoForm',

  components: { TextInput, Submit, ValidationObserver, ValidationProvider },

  props: {
    initialFields: {
      type: Object,
      required: true,
    },
  },

  data() {
    return {
      currentFields: this.buildCurrentFields(),
    };
  },

  computed: {
    showEmailConfirmation() {
      return this.currentFields.email.flags.changed;
    },

    hasChanged() {
      const haveChanged = Object.keys(this.currentFields).filter(
        key => this.currentFields[key].flags.changed
      );

      return haveChanged.length > 0;
    },

    isValid() {
      const areNotValid = Object.keys(this.currentFields).filter(
        key => !this.currentFields[key].flags.valid
      );

      return areNotValid.length === 0;
    },
  },

  watch: {
    showEmailConfirmation() {
      this.currentFields.confirmedEmail.value = '';
    },

    hasChanged(newHasChanged, oldHasChanged) {
      if (newHasChanged !== oldHasChanged) {
        this.$emit('onHasChangedToggle', newHasChanged);
      }
    },

    initialFields() {
      this.currentFields = this.buildCurrentFields();
    },
  },

  methods: {
    buildCurrentFields() {
      const final = {};

      Object.keys(this.initialFields).forEach(key => {
        final[key] = {
          value: this.initialFields[key],
          flags: { changed: false, valid: true },
        };
      });

      return final;
    },

    addFlags(name, flags) {
      this.currentFields[name].flags = { ...flags };
    },
  },
};
</script>
