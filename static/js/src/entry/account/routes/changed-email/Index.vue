<template>
  <div>
    <basic-nav-bar />

    <main class="l-minimal has-bg-white-off has-xl-padding">
      <div class="l-minimal__content">
        <h1 class="has-xl-btm-marg">Please verify your email address change</h1>
        <p class="has-b-btm-marg t-size-b">
          Thanks for updating your account information! To log back into your
          account, we need you to verify your new email address.
        </p>
        <contact-us
          :ga-label="ga.userPortal.labels['changed-email']"
          :display="{ color: 'black' }"
        >
          <template #text>
            Check your inbox for an email from The Texas Tribune with the
            subject line "Please confirm your login email change," then click to
            verify your email. Having trouble? Contact
          </template>
        </contact-us>
      </div>
    </main>

    <basic-site-footer />
  </div>
</template>

<script>
import routeMixin from '../mixin';

import ContactUs from '../../components/ContactUsSmall.vue';

export default {
  name: 'ChangedEmailRoute',

  components: { ContactUs },

  mixins: [routeMixin],
};
</script>
