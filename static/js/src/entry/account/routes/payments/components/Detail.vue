<template>
  <div>
    <div class="has-xxl-btm-marg"><payment-list :payments="data" /></div>

    <p class="t-size-xs t-links-underlined has-text-gray-dark">
      Note: Donation history does not include event sponsorships or ticket
      purchases. To receive a {{ lastYear }} tax receipt with this information,
      please contact
      <a
        href="mailto:community@texastribune.org"
        ga-on="click"
        :ga-event-category="ga.userPortal.category"
        :ga-event-action="ga.userPortal.actions['contact-us']"
        :ga-event-label="ga.userPortal.labels.payments"
        >community@texastribune.org</a
      >.
    </p>
  </div>
</template>

<script>
import getYear from 'date-fns/get_year';

import PaymentList from '../../../components/PaymentList.vue';

export default {
  name: 'PaymentsDetail',

  components: { PaymentList },

  props: {
    data: {
      type: Array,
      required: true,
    },
  },

  computed: {
    lastYear() {
      return getYear(new Date()) - 1;
    },
  },
};
</script>
