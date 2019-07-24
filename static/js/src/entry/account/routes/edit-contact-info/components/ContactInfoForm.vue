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
    >
      <text-input
        v-model="firstName"
        :error-messages="errors"
        label="First name"
        name="firstName"
      />
    </validation-provider>
    <validation-provider
      v-slot="{ errors }"
      name="lastName"
      :rules="{ required: true }"
    >
      <text-input
        v-model="lastName"
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
    >
      <text-input
        v-model="email"
        :error-messages="errors"
        label="Email"
        name="email"
      />
    </validation-provider>
    <validation-provider
      v-if="showEmailConfirmation"
      v-slot="{ errors }"
      name="confirmedEmail"
      :rules="{ required: true, is: email }"
      immediate
    >
      <text-input
        v-model="confirmedEmail"
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
    >
      <text-input
        v-model="zip"
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
          v-model="marketing"
          type="checkbox"
          name="marketing"
        />
        Yes, I would like to receive emails with special promotions, product
        announcements and membership opportunities.
      </label>
    </div>
    <submit :disabled="invalid" />
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
      ...this.initialValues,
      confirmedEmail: '',
      showEmailConfirmation: false,
    };
  },

  watch: {
    async email() {
      const { valid } = await this.$refs.email.validate();

      if (this.emailDidChange() && valid) {
        this.showEmailConfirmation = true;
      } else {
        this.showEmailConfirmation = false;
        this.confirmedEmail = '';
      }
    },
  },

  methods: {
    emailDidChange() {
      const { value, initialValue } = this.$refs.email;
      return value !== initialValue;
    },

    async onSubmit() {
      const { email, firstName, lastName, zip, marketing } = this;
      const identityPayload = { tribune_offers_consent: marketing };
      const userPayload = {
        first_name: firstName,
        last_name: lastName,
        postal_code: zip,
      };

      if (this.emailDidChange()) identityPayload.email = email;

      this.$emit('updateContactInfo', { userPayload, identityPayload });
    },
  },
};
</script>
