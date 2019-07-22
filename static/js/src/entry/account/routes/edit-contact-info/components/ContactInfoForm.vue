<template>
  <form @submit.prevent="onSubmit">
    <div>
      <label for="first-name">First name</label>
      <input
        id="first-name"
        v-model="firstName"
        v-validate.initial="firstNameValidation"
        type="text"
        name="firstName"
      />
      <span>{{ errors.first('firstName') }}</span>
    </div>
    <div>
      <label for="last-name">Last name</label>
      <input
        id="last-name"
        v-model="lastName"
        v-validate.initial="lastNameValidation"
        type="text"
        name="lastName"
      />
      <span>{{ errors.first('lastName') }}</span>
    </div>
    <div>
      <label for="email">Email</label>
      <input
        id="email"
        v-model="email"
        v-validate.initial="emailValidation"
        type="email"
        name="email"
      />
      <span>{{ errors.first('email') }}</span>
    </div>
    <div v-show="showEmailConfirmation">
      <label for="confirmed-email"
        >Type your email again to confirm the change</label
      >
      <input
        id="confirmed-email"
        key="confirmed-email"
        v-model="confirmedEmail"
        v-validate.initial="
          showEmailConfirmation ? confirmedEmailValidation : false
        "
        type="text"
        name="confirmedEmail"
        @paste.prevent
      />
      <span>{{ errors.first('confirmedEmail') }}</span>
    </div>
    <div>
      <label for="zip">ZIP code</label>
      <input
        id="zip"
        v-model="zip"
        v-validate.initial="zipValidation"
        type="text"
        name="zip"
      />
      <span>{{ errors.first('zip') }}</span>
    </div>
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
    <input :disabled="isDisabled" type="submit" value="Submit" />
  </form>
</template>

<script>
export default {
  name: 'ContactInfoForm',

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
    };
  },

  computed: {
    showEmailConfirmation() {
      const { fields } = this;
      if (!fields || !Object.keys(fields).length) return false;

      const { changed, valid } = fields.email;
      return changed && valid;
    },

    isDisabled() {
      return this.errors.items.length > 0;
    },

    firstNameValidation() {
      return { required: true };
    },

    lastNameValidation() {
      return { required: true };
    },

    emailValidation() {
      return { required: true, email: true };
    },

    confirmedEmailValidation() {
      return { required: true, is: this.email };
    },

    zipValidation() {
      return { required: true };
    },
  },

  watch: {
    showEmailConfirmation() {
      this.confirmedEmail = '';
    },
  },

  methods: {
    async onSubmit() {
      const { changed: emailChanged } = this.fields.email;
      const { email, firstName, lastName, zip, marketing } = this;
      const identityPayload = { tribune_offers_consent: marketing };
      const userPayload = {
        first_name: firstName,
        last_name: lastName,
        postal_code: zip,
      };

      if (emailChanged) identityPayload.email = email;

      this.$emit('updateContactInfo', {
        userPayload,
        identityPayload,
      });
    },
  },
};
</script>
