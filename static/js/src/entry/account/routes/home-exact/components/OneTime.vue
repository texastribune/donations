<template>
  <summary-box heading="membership" :display="{ isExpired: false }">
    <template v-slot:content>
      <p
        v-if="lastTransaction.last4"
        class="has-text-gray-dark t-space-heading-m"
      >
        Thank you for being a Texas Tribune member! Your last donation of
        <strong>${{ lastTransaction.amount }}</strong> was charged on
        <strong>{{ lastTransaction.date }}</strong> to your card ending in
        <strong>{{ lastTransaction.last4 }}</strong
        >.
      </p>
      <p v-else class="has-text-gray-dark t-space-heading-m">
        Thank you for being a Texas Tribune member! Your last donation of
        <strong>${{ lastTransaction.amount }}</strong> was charged on
        <strong>{{ lastTransaction.date }}</strong
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
        <li class="has-m-btm-marg">
          <span class="c-link-list__arrow has-text-teal">
            <strong>&rarr;</strong>
          </span>
          <span class="has-text-gray-dark">
            <router-link :to="{ name: 'membership' }"
              >More about your membership</router-link
            >
          </span>
        </li>
        <li>
          <span class="c-link-list__arrow has-text-teal">
            <strong>&rarr;</strong>
          </span>
          <span class="has-text-gray-dark">
            <a href="#">Become a sustaining member</a>
          </span>
        </li>
      </ul>
    </template>
  </summary-box>
</template>

<script>
import SummaryBox from '../../../components/SummaryBox.vue';

export default {
  name: 'OneTime',

  components: { SummaryBox },

  props: {
    lastTransaction: {
      type: Object,
      required: true,
    },
  },
};
</script>
