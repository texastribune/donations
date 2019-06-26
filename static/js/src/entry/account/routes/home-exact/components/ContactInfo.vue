<template>
  <summary-box heading="contact info">
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
      <ul
        v-if="!pwResetSuccess && !pwResetFailure"
        :style="[
          isStaff && { 'pointer-events': 'none' },
          isStaff && { opacity: '.2' },
        ]"
        class="c-link-list"
      >
        <li>
          <span class="c-link-list__arrow has-text-teal">
            <strong>&rarr;</strong>
          </span>
          <span class="has-text-gray-dark">
            <button class="c-link-button" @click="$emit('resetPassword')">
              Reset your password
            </button>
          </span>
        </li>
      </ul>
      <p
        v-else-if="pwResetSuccess"
        class="t-size-xs t-space-heading-m has-text-gray"
      >
        Check your inbox for an email from The Texas Tribune with the subject
        line &quot;Reset your password.&quot;
      </p>
      <p v-else class="t-size-xs t-space-heading-m has-text-gray">
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
  name: 'ContactInfo',

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
};
</script>
