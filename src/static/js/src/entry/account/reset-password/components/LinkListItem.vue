<template>
  <reset-password-provider
    v-slot="{ pwReset: { pwResetSuccess, pwResetFailure, pwReset } }"
  >
    <link-list-item>
      <template #main>
        <button class="c-link-button" @click="pwReset(gaLabel)">
          Reset your password
        </button>
      </template>
      <template #extra>
        <p v-if="pwResetSuccess" class="t-size-xs has-text-gray-dark">
          Check your inbox for an email from The Texas Tribune with the subject
          line &quot;Reset your password.&quot;
        </p>
        <p v-if="pwResetFailure" class="t-size-xs has-text-gray-dark">
          There was an issue resetting your password. If you continue having
          trouble, email
          <a href="mailto:community@texastribune.org"
            >community@texastribune.org </a
          >.
        </p>
      </template>
    </link-list-item>
  </reset-password-provider>
</template>

<script>
import ResetPasswordProvider from '../providers/ResetPasswordProvider.vue';

import LinkListItem from '../../components/LinkListItem.vue';

export default {
  name: 'LinkListItemResetPassword',

  components: { ResetPasswordProvider, LinkListItem },

  props: {
    gaLabel: {
      type: String,
      required: true,
    },
  },
};
</script>
