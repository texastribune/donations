<template>
  <link-email-provider
    ref="provider"
    v-slot="{ linkedEmails, initialFields, submittedEmail }"
  >
    <div class="c-link-email t-linkstyle--underlined">
      <template v-if="submittedEmail">
        <h2 class="t-size-b has-b-btm-marg">Verify your linked email</h2>
        <p class="t-size-xs has-text-gray has-s-btm-marg">
          To keep your information safe, we need you to verify your linked
          email: <strong>{{ submittedEmail }}</strong
          >.
        </p>
        <p class="t-size-xs has-text-gray">
          Check your inbox for an email from The Texas Tribune with subject line
          "Link your account," then click to verify. Having trouble? Email
          <a href="mailto:community@texastribune.org"
            >community@texastribune.org</a
          >.
        </p>
      </template>
      <template v-else>
        <div class="has-xxxs-btm-marg">
          <slot name="heading">
            <h2 class="t-size-b">Not seeing your donations?</h2>
          </slot>
        </div>
        <div class="has-b-btm-marg">
          <slot name="text" :linked-emails="linkedEmails | formatLinkedEmails">
            <p class="t-size-xs has-text-gray">
              You're seeing donations for
              {{ linkedEmails | formatLinkedEmails }}. You may have donated with
              a different email address. Enter another email below to link your
              accounts.
            </p>
          </slot>
        </div>
        <div class="has-b-btm-marg">
          <text-input-and-submit
            :initial-fields="initialFields"
            @onSubmit="linkEmail"
          />
        </div>
        <p class="t-size-xs has-text-gray">
          Already tried this? Still not seeing your donations? Contact us at
          <a href="mailto:membership@texastribune.org"
            >membership@texastribune.org</a
          >.
        </p>
      </template>
    </div>
  </link-email-provider>
</template>

<script>
import LinkEmailProvider from '../providers/LinkEmailProvider.vue';
import TextInputAndSubmit from '../../../components/TextInputAndSubmit.vue';

export default {
  name: 'LinkEmail',

  components: { LinkEmailProvider, TextInputAndSubmit },

  filters: {
    formatLinkedEmails(emails) {
      let formatted = '';

      emails.forEach((email, index) => {
        if (emails.length === 1) {
          formatted += email;
        } else if (index === emails.length - 1) {
          formatted += ` and ${email}`;
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
