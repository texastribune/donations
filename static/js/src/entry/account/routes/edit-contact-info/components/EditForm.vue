<template>
  <form :key="formKey" @submit.prevent="$emit('onSubmit', currentFields)">
    <validation-provider
      v-slot="{ errors, flags }"
      :rules="currentFields.firstName.rules"
      name="firstName"
      immediate
    >
      <text-input
        v-model="currentFields.firstName.value"
        :error-messages="errors"
        :flags="flags"
        label="First name"
        name="firstName"
        @updateFlags="updateFlags"
      />
    </validation-provider>
    <validation-provider
      v-slot="{ errors, flags }"
      :rules="currentFields.lastName.rules"
      name="lastName"
      immediate
    >
      <text-input
        v-model="currentFields.lastName.value"
        :error-messages="errors"
        :flags="flags"
        label="Last name"
        name="lastName"
        @updateFlags="updateFlags"
      />
    </validation-provider>
    <validation-provider
      v-slot="{ errors, flags }"
      :rules="currentFields.email.rules"
      name="email"
      immediate
    >
      <text-input
        v-model="currentFields.email.value"
        :error-messages="errors"
        :flags="flags"
        label="Email"
        name="email"
        @updateFlags="updateFlags"
      >
        <p v-show="showConfirmedEmail" class="has-text-error">
          <strong>Are you sure?</strong> Changing this will log you out of your
          account, and you won't be able to log back in with
          <strong>Foobar</strong>. Changing your account email will not affect
          your email subscriptions.
        </p>
        <p v-show="!showConfirmedEmail">
          Notice: This email is for logging into your account. Changing it will
          not affect your email newsletters.
        </p>
      </text-input>
    </validation-provider>
    <validation-provider
      v-show="showConfirmedEmail"
      v-slot="{ errors, flags }"
      :rules="confirmedEmailRules"
      name="confirmedEmail"
      immediate
    >
      <text-input
        v-model="currentFields.confirmedEmail.value"
        :error-messages="errors"
        :flags="flags"
        label="Type your email again to confirm the change"
        name="confirmedEmail"
        prevent-paste
        @updateFlags="updateFlags"
      />
    </validation-provider>
    <validation-provider
      v-slot="{ errors, flags }"
      :rules="currentFields.zip.rules"
      name="zip"
      immediate
    >
      <text-input
        v-model="currentFields.zip.value"
        :error-messages="errors"
        :flags="flags"
        label="ZIP code"
        name="zip"
        @updateFlags="updateFlags"
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
    <submit :disabled="!formIsValid" />
  </form>
</template>

<script>
import formMixin from '../../../mixins/form';

export default {
  name: 'EditContactInfoForm',

  mixins: [formMixin],

  computed: {
    emailHasChangedAndIsValid() {
      const { changed, valid } = this.currentFields.email;
      return changed && valid;
    },

    showConfirmedEmail: {
      get() {
        const { isVisible } = this.currentFields.confirmedEmail;
        return isVisible;
      },

      set(isVisible) {
        this.currentFields.confirmedEmail.isVisible = isVisible;
      },
    },

    confirmedEmailRules() {
      return { required: true, is: this.currentFields.email.value };
    },
  },

  watch: {
    emailHasChangedAndIsValid(newHasChangedAndIsValid) {
      if (newHasChangedAndIsValid) {
        this.showConfirmedEmail = true;
      } else {
        this.showConfirmedEmail = false;
        this.resetValue('confirmedEmail');
      }
    },
  },
};
</script>
