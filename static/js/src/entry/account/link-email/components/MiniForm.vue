<template>
  <link-email-provider
    v-slot="{ linkEmail, linkedEmails, initialFields, submittedEmail }"
    :ga-label="gaLabel"
  >
    <div class="c-link-email t-links-underlined">
      <template v-if="submittedEmail">
        <h2 class="t-size-b has-b-btm-marg">Verify your email</h2>
        <p class="t-size-xs has-text-gray has-s-btm-marg">
          To keep your information safe, we need you to verify
          <strong>{{ submittedEmail }}</strong> before we can update your
          account.
        </p>
        <p class="t-size-xs has-text-gray">
          Check your inbox for an email from The Texas Tribune with the subject
          line "Link your account" and click to verify.
        </p>
      </template>
      <template v-else>
        <div class="has-xxxs-btm-marg">
          <slot name="heading">
            <h2 class="t-size-b t-uppercase">Missing donations?</h2>
          </slot>
        </div>
        <div class="has-b-btm-marg">
          <slot name="text" :linked-emails="linkedEmails | formatLinkedEmails">
            <p class="t-size-xs has-text-gray-dark">
              You're seeing donations from:
              <strong>{{ linkedEmails | formatLinkedEmails }}</strong
              >. You may have donated with a different email address. Enter
              another email below to link your accounts.
            </p>
          </slot>
        </div>
        <text-input-and-submit
          name="linkEmail"
          label="Email address to link"
          rules="required|email"
          :initial-fields="initialFields"
          @onSubmit="linkEmail"
        />
      </template>
    </div>
  </link-email-provider>
</template>

<script>
import { localize } from 'vee-validate';

import LinkEmailProvider from '../providers/LinkEmailProvider.vue';

import TextInputAndSubmit from '../../form/components/TextInputAndSubmit.vue';

localize({
  en: {
    fields: {
      linkEmail: {
        required: 'This field must contain a valid email address.',
        email: 'This field must contain a valid email address.',
      },
    },
  },
});

export default {
  name: 'MiniFormLinkEmail',

  components: { LinkEmailProvider, TextInputAndSubmit },

  filters: {
    formatLinkedEmails(emails) {
      let formatted = '';

      emails.forEach((email, index) => {
        if (index === emails.length - 1) {
          formatted += `${email}`;
        } else {
          formatted += `${email}, `;
        }
      });

      return formatted;
    },
  },

  props: {
    gaLabel: {
      type: String,
      required: true,
    },
  },
};
</script>
