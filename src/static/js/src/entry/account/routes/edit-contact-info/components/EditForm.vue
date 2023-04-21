<template>
  <validation-observer v-slot="{ handleSubmit }">
    <form :key="formKey" @submit.prevent="handleSubmit(onSubmit)">
      <p v-if="badEmail" role="alert" class="has-b-btm-marg has-text-error">
        <strong
          >Error: You can't change your login email to {{ badEmail }} because an
          account already exists with that email address.</strong
        >
      </p>
      <p
        v-if="showSuccess"
        role="alert"
        class="has-b-btm-marg has-text-success"
      >
        <strong>Success! Your profile has been updated.</strong>
      </p>
      <validation-provider
        v-slot="{ errors, pristine, changed, valid }"
        rules="required"
        name="firstName"
        slim
      >
        <div class="has-b-btm-marg">
          <text-input
            v-model="currentFields.firstName.value"
            label="First name"
            name="firstName"
            :error-messages="errors"
            :pristine="pristine"
            :changed="changed"
            :valid="valid"
            @updateFlags="updateFlags"
          />
        </div>
      </validation-provider>
      <validation-provider
        v-slot="{ errors, pristine, changed, valid }"
        rules="required"
        name="lastName"
        slim
      >
        <div class="has-b-btm-marg">
          <text-input
            v-model="currentFields.lastName.value"
            label="Last name"
            name="lastName"
            :error-messages="errors"
            :pristine="pristine"
            :changed="changed"
            :valid="valid"
            @updateFlags="updateFlags"
          />
        </div>
      </validation-provider>
      <validation-provider
        v-slot="{ errors, pristine, changed, valid }"
        rules="required|email"
        name="email"
        slim
      >
        <div class="has-b-btm-marg">
          <text-input
            v-model="currentFields.email.value"
            label="Login email"
            name="email"
            :error-messages="errors"
            :pristine="pristine"
            :changed="changed"
            :valid="valid"
            @updateFlags="updateFlags"
          >
            <template #extra>
              <p v-show="showConfirmedEmail" class="t-size-xs has-text-error">
                <strong>Are you sure?</strong> Changing this email will
                immediately log you out of texastribune.org, and you won't be
                able to log back in with
                <strong>{{ initialFields.email }}</strong
                >.
              </p>
            </template>
          </text-input>
        </div>
      </validation-provider>
      <validation-provider
        v-show="showConfirmedEmail"
        v-slot="{ errors, pristine, changed, valid }"
        :rules="confirmedEmailRules"
        name="confirmedEmail"
        slim
      >
        <div class="has-b-btm-marg">
          <text-input
            v-model="currentFields.confirmedEmail.value"
            label="Type your email again to confirm this change"
            name="confirmedEmail"
            prevent-paste
            :error-messages="errors"
            :pristine="pristine"
            :changed="changed"
            :valid="valid"
            @updateFlags="updateFlags"
          />
        </div>
      </validation-provider>
      <validation-provider
        v-slot="{ errors, pristine, changed, valid }"
        rules="required|numeric"
        name="zip"
        slim
      >
        <div class="has-b-btm-marg">
          <text-input
            v-model="currentFields.zip.value"
            label="ZIP code"
            name="zip"
            :error-messages="errors"
            :pristine="pristine"
            :changed="changed"
            :valid="valid"
            @updateFlags="updateFlags"
          />
        </div>
      </validation-provider>
      <validation-provider
        v-slot="{ errors, pristine, changed, valid }"
        name="marketing"
        slim
      >
        <div class="has-b-btm-marg">
          <checkbox
            v-model="currentFields.marketing.value"
            label="Yes, I'd like to be among the first to know about special announcements, events and membership news from the Tribune. (Remember: Per our privacy policy, we won't share your data without permission.)"
            name="marketing"
            :error-messages="errors"
            :pristine="pristine"
            :changed="changed"
            :valid="valid"
            @updateFlags="updateFlags"
          />
        </div>
      </validation-provider>

      <submit value="Save" />
    </form>
  </validation-observer>
</template>

<script>
import { localize } from 'vee-validate';

import formMixin from '../../../form/mixins/form';

localize({
  en: {
    fields: {
      email: {
        required: 'You must have an email to log into texastribune.org.',
        email: 'Please enter a valid email address.',
      },

      confirmedEmail: {
        required: 'Email addresses do not match.',
        email: 'Email addresses do not match.',
        confirm: 'Email addresses do not match.',
      },

      firstName: {
        required:
          'Please provide your first and last name. They appear with comments on texastribune.org to promote a more transparent and personable atmosphere.',
      },

      lastName: {
        required:
          'Please provide your first and last name. They appear with comments on texastribune.org to promote a more transparent and personable atmosphere.',
      },

      zip: {
        required:
          'Please enter your ZIP code to help us inform you about news and events in your area.',
        numeric: 'Your ZIP code must contain only numbers.',
      },
    },
  },
});

export default {
  name: 'EditContactInfoForm',

  mixins: [formMixin],

  props: {
    badEmail: {
      type: String,
      required: true,
    },

    showSuccess: {
      type: Boolean,
      required: true,
    },
  },

  computed: {
    showConfirmedEmail() {
      const { changed, valid } = this.currentFields.email;

      return changed && valid;
    },

    confirmedEmailRules() {
      if (this.showConfirmedEmail) {
        return 'required|email|confirm:@email';
      }

      return '';
    },
  },

  watch: {
    showConfirmedEmail(newShowConfirmed, oldShowConfirmed) {
      if (!newShowConfirmed && oldShowConfirmed) {
        this.emptyOutField('confirmedEmail');
      }
    },
  },
};
</script>
