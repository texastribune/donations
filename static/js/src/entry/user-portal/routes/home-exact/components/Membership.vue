<template>
  <summary-box heading="membership" :display="{ isExpired: false }">
    <template v-slot:content>
      <p class="has-text-gray-dark t-space-heading-m">
        Thank you for being a Texas Tribune member! Your next
        {{ nextTransaction.period }} donation of
        <strong>${{ nextTransaction.amount }}</strong> will be charged on
        <strong>{{ nextTransaction.date }}</strong> to your card ending in
        <strong>{{ nextTransaction.last4 }}</strong
        >.
      </p>
    </template>
    <template v-slot:links>
      <ul class="c-link-list">
        <li class="has-m-btm-marg">
          <span class="c-link-list__arrow has-text-teal">
            <strong>&rarr;</strong>
          </span>
          <span class="has-text-gray-dark">
            <router-link :to="{ name: 'payments' }"
              >See your donation history</router-link
            >
          </span>
        </li>
        <li>
          <span class="c-link-list__arrow has-text-teal">
            <strong>&rarr;</strong>
          </span>
          <span class="has-text-gray-dark">
            <router-link :to="{ name: 'membership' }"
              >More about your membership</router-link
            >
          </span>
        </li>
      </ul>
    </template>
    <template v-slot:bottom>
      <p class="has-text-gray-dark t-space-heading-m t-linkstyle--underlined">
        To update your membership status, contact us at
        <a href="mailto:community@texastribune.org"
          >community@texastribune.org</a
        >.
      </p>
    </template>
  </summary-box>
</template>

<script>
import SummaryBox from '../../../components/SummaryBox.vue';

export default {
  name: 'Membership',

  components: { SummaryBox },

  props: {
    nextTransaction: {
      type: Object,
      required: true,
    },
  },
};
</script>
