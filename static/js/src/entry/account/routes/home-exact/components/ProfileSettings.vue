<template>
  <summary-box heading="profile settings">
    <template v-slot:content>
      <info-list :items="contactInfo">
        <template v-slot="slotProps">
          <span
            class="has-text-gray-dark"
            :class="{ 't-wrap-break': slotProps.item.heading === 'Email' }"
          >
            {{ slotProps.item.text }}
          </span>
        </template>
      </info-list>
    </template>

    <template v-slot:links>
      <ul class="c-link-list">
        <li class="has-m-btm-marg">
          <span class="c-link-list__arrow has-text-teal">
            <strong>&rarr;</strong>
          </span>
          <span class="has-text-gray-dark">
            <router-link
              ga-on="click"
              :to="{ name: 'edit-contact-info' }"
              :ga-event-category="ga.userPortalNav.category"
              :ga-event-action="ga.userPortalNav.actions.inline"
              :ga-event-label="ga.userPortalNav.labels['edit-contact-info']"
            >
              Edit your profile
            </router-link>
          </span>
        </li>
        <li
          v-if="!pwResetSuccess && !pwResetFailure"
          :style="[
            isStaff && { 'pointer-events': 'none' },
            isStaff && { opacity: '.2' },
          ]"
        >
          <span class="c-link-list__arrow has-text-teal">
            <strong>&rarr;</strong>
          </span>
          <span class="has-text-gray-dark">
            <button class="c-link-button" @click="resetPassword">
              Reset your password
            </button>
          </span>
        </li>
      </ul>
      <p v-if="pwResetSuccess" class="t-size-xs has-text-gray">
        Check your inbox for an email from The Texas Tribune with the subject
        line &quot;Reset your password.&quot;
      </p>
      <p v-if="pwResetFailure" class="t-size-xs has-text-gray">
        There was an issue resetting your password. If you continue having
        trouble, email
        <a href="mailto:community@texastribune.org"
          >community@texastribune.org </a
        >.
      </p>
    </template>
  </summary-box>
</template>

<script>
import SummaryBox from '../../../components/SummaryBox.vue';
import InfoList from '../../../components/InfoList.vue';

export default {
  name: 'SummaryProfileSettings',

  components: { SummaryBox, InfoList },

  props: {
    contactInfo: {
      type: Array,
      required: true,
    },

    pwResetSuccess: {
      type: Boolean,
      required: true,
    },

    pwResetFailure: {
      type: Boolean,
      required: true,
    },

    isStaff: {
      type: Boolean,
      required: true,
    },
  },

  methods: {
    resetPassword() {
      this.$emit('resetPassword');

      window.dataLayer.push({
        event: this.ga.customEventName,
        gaCategory: this.ga.userPortal.category,
        gaAction: this.ga.userPortal.actions['reset-password'],
        gaLabel: this.ga.userPortal.labels.home,
      });
    },
  },
};
</script>
