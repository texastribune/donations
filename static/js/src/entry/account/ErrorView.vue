<template>
  <div>
    <basic-nav-bar />

    <main class="l-minimal has-bg-white-off has-xl-padding">
      <div class="l-minimal__content t-links-underlined">
        <h1 class="has-xl-btm-marg">
          <template v-if="isUnverifiedError">
            Please verify your account.
          </template>
          <template v-else>
            Sorry about that.
          </template>
        </h1>

        <p class="has-s-btm-marg">
          <template v-if="isUnverifiedError">
            Thanks for creating a Texas Tribune account &mdash; you’re almost
            done! To view your account, we need you to verify your email
            address: <strong>{{ user.email }}</strong
            >. Check your inbox for an email from The Texas Tribune with the
            subject line &quot;Please confirm your account,&quot; then click to
            verify your email.
          </template>
          <template v-else>
            We’re having trouble loading your account information, and we're
            working hard to fix it. Click here to return to your
            <a href="/account/">account overview</a>.
          </template>
        </p>

        <p>
          Having trouble? Contact
          <a
            href="mailto:community@texastribune.org?subject=account%20technical%20error"
            ga-on="click"
            :ga-event-category="ga.userPortal.category"
            :ga-event-action="ga.userPortal.actions['contact-us']"
            :ga-event-label="gaLabel"
            >community@texastribune.org</a
          >.
        </p>
      </div>
    </main>

    <basic-site-footer />
  </div>
</template>

<script>
import contextMixin from './store/context/mixin';
import userMixin from './store/user/mixin';
import { UnverifiedError } from './errors';
import setTitle from './utils/set-title';

export default {
  name: 'ErrorView',

  mixins: [contextMixin, userMixin],

  computed: {
    isUnverifiedError() {
      return this.context.error instanceof UnverifiedError;
    },

    gaLabel() {
      if (this.isUnverifiedError) {
        return this.ga.userPortal.labels.unverified;
      }
      return this.ga.userPortal.labels.error;
    },
  },

  mounted() {
    window.onpopstate = () => {
      window.location.reload();
    };

    setTitle('Error');
  },
};
</script>
