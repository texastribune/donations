<template>
  <summary-box heading="membership" :display="{ isExpired: true }">
    <template v-slot:content>
      <p class="has-text-gray-dark t-space-heading-m">
        <span class="has-text-error"
          >Your membership expired on <strong>{{ expirationDate }}</strong
          >.</span
        >
        <template v-if="lastTransaction.last4">
          Your last donation of
          <strong>${{ lastTransaction.amount }}</strong> was charged on
          <strong>{{ lastTransaction.date }}</strong> to your card ending in
          <strong>{{ lastTransaction.last4 }}</strong
          >.
        </template>
        <template v-else>
          Your last donation of
          <strong>${{ lastTransaction.amount }}</strong> was charged on
          <strong>{{ lastTransaction.date }}</strong
          >.
        </template>
      </p>
    </template>
    <template v-slot:links>
      <ul class="c-link-list">
        <li class="has-m-btm-marg">
          <span class="c-link-list__arrow has-text-teal">
            <strong>&rarr;</strong>
          </span>
          <span class="has-text-gray-dark">
            <a href="#">Renew your membership</a>
          </span>
        </li>
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
  </summary-box>
</template>

<script>
import SummaryBox from '../../../components/SummaryBox.vue';

export default {
  name: 'MembershipExpired',

  components: { SummaryBox },

  props: {
    lastTransaction: {
      type: Object,
      required: true,
    },

    expirationDate: {
      type: String,
      required: true,
    },
  },
};
</script>
