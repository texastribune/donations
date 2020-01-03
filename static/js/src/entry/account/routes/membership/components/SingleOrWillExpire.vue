<template>
  <section class="c-detail-box">
    <div class="has-xxl-btm-marg"><info-list :items="data" /></div>

    <user-internal-nav show-become-sustaining show-donation-history />
  </section>
</template>

<script>
import InfoList from '../../../components/InfoList.vue';

export default {
  name: 'MembershipSingleOrWillExpire',

  components: { InfoList },

  props: {
    data: {
      type: Array,
      required: true,
    },

    isSingleDonor: {
      type: Boolean,
      required: true,
    },
  },
};
</script>
