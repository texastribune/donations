<template>
  <link-email-provider
    ref="provider"
    v-slot="{ linkedEmails, initialFields, submittedEmail }"
  >
    <div class="c-link-email t-linkstyle--underlined">
      <template v-if="submittedEmail">
        <h2 class="t-size-b has-b-btm-marg">Verify your email</h2>
        <p class="t-size-xs has-text-gray has-s-btm-marg">
          To keep your information safe, we need you to verify
          <strong>{{ submittedEmail }}</strong> before we can update your
          account.
        </p>
        <p class="t-size-xs has-text-gray">
          Check your inbox for an email from The Texas Tribune with the subject
          line "Was this you?" and click to verify.
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
            <p class="t-size-xs has-text-gray">
              You're seeing donations from:
              <strong>{{ linkedEmails | formatLinkedEmails }}</strong
              >. You may have donated with a different email address. Enter
              another email below to link your accounts.
            </p>
          </slot>
        </div>
        <text-input-and-submit
          :initial-fields="initialFields"
          @onSubmit="linkEmail"
        />
      </template>
    </div>
  </link-email-provider>
</template>

<script>
import LinkEmailProvider from '../providers/LinkEmailProvider.vue';
import TextInputAndSubmit from '../../../form/components/TextInputAndSubmit.vue';

export default {
  name: 'LinkEmail',

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

  methods: {
    async linkEmail(fields) {
      await this.$refs.provider.linkEmail(fields);

      window.dataLayer.push({
        event: this.ga.customEventName,
        gaCategory: this.ga.userPortal.category,
        gaAction: this.ga.userPortal.actions['submit-linked-email'],
        gaLabel: this.gaLabel,
      });
    },
  },
};
</script>
