<template>
  <validation-observer
    v-slot="{ invalid }"
    tag="form"
    @submit.prevent="onSubmit"
  >
    <validation-provider
      v-slot="{ errors }"
      name="firstName"
      :rules="{ required: true }"
      immediate
    >
      <text-input
        v-model="formFields.firstName"
        :error-messages="errors"
        label="First name"
        name="firstName"
      />
    </validation-provider>
    <validation-provider
      v-slot="{ errors }"
      name="lastName"
      :rules="{ required: true }"
      immediate
    >
      <text-input
        v-model="formFields.lastName"
        :error-messages="errors"
        label="Last name"
        name="lastName"
      />
    </validation-provider>
    <validation-provider
      ref="email"
      v-slot="{ errors }"
      name="email"
      :rules="{ required: true, email: true }"
      immediate
    >
      <text-input
        v-model="formFields.email"
        :error-messages="errors"
        label="Email"
        name="email"
      >
        <p v-show="showEmailConfirmation" class="has-text-error">
          <strong>Are you sure?</strong> Changing this will log you out of your
          account, and you won't be able to log back in with
          <strong>{{ originalValues.email }}</strong
          >. Changing your account email will not affect your email
          subscriptions.
        </p>
        <p v-show="!showEmailConfirmation">
          Notice: This email is for logging into your account. Changing it will
          not affect your email newsletters.
        </p>
      </text-input>
    </validation-provider>
    <validation-provider
      v-if="showEmailConfirmation"
      v-slot="{ errors }"
      name="confirmedEmail"
      :rules="{ required: true, is: email }"
      immediate
    >
      <text-input
        v-model="formFields.confirmedEmail"
        :error-messages="errors"
        label="Type your email again to confirm the change"
        name="confirmedEmail"
        prevent-paste
      />
    </validation-provider>
    <validation-provider
      v-slot="{ errors }"
      name="zip"
      :rules="{ required: true }"
      immediate
    >
      <text-input
        v-model="formFields.zip"
        :error-messages="errors"
        label="ZIP code"
        name="zip"
      />
    </validation-provider>
    <div>
      <label for="marketing">News & Offers</label>
      <label for="marketing">
        <input
          id="marketing"
          v-model="formFields.marketing"
          type="checkbox"
          name="marketing"
        />
        Yes, I would like to receive emails with special promotions, product
        announcements and membership opportunities.
      </label>
    </div>
    <submit v-if="invalid !== undefined" :disabled="invalid" />
  </validation-observer>
</template>

<script>
import { ValidationObserver, ValidationProvider } from 'vee-validate';

import TextInput from '../../../components/TextInput.vue';
import Submit from '../../../components/Submit.vue';

export default {
  name: 'ContactInfoForm',

  components: { TextInput, Submit, ValidationObserver, ValidationProvider },

  props: {
    initialValues: {
      type: Object,
      required: true,
    },
  },

  data() {
    return {
      formFields: { ...this.initialValues, confirmedEmail: '' },
      originalValues: { ...this.initialValues },
      showEmailConfirmation: false,
    };
  },

  computed: {
    emailChanged() {
      const { email: newEmail } = this.formFields;
      const { email: originalEmail } = this.originalValues;
      return newEmail !== originalEmail;
    },

    email() {
      // just for the watcher
      return this.formFields.email;
    },
  },

  watch: {
    async email() {
      const { valid } = await this.$refs.email.validate();
      const { emailChanged } = this;

      if (emailChanged && valid) {
        this.showEmailConfirmation = true;
      } else {
        this.showEmailConfirmation = false;
        this.formFields.confirmedEmail = '';
      }
    },
  },

  methods: {
    async onSubmit() {
      const { emailChanged } = this;
      const { email, firstName, lastName, zip, marketing } = this.formFields;
      const identityPayload = { tribune_offers_consent: marketing };
      const userPayload = {
        first_name: firstName,
        last_name: lastName,
        postal_code: zip,
      };

      if (emailChanged) identityPayload.email = email;

      this.$emit('updateContactInfo', { userPayload, identityPayload });
    },
  },
};
</script>
