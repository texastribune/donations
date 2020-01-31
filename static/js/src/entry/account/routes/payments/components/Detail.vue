<template>
  <user-provider v-slot="{ user: { pastTransactions } }">
    <div>
      <div class="has-xxl-btm-marg">
        <payment-list :payments="pastTransactions" />
      </div>

      <p class="t-size-xs t-links-underlined has-text-gray-dark">
        Note: Donation history does not include event sponsorships or ticket
        purchases. To receive a {{ lastYear }} tax receipt with this
        information, please contact
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
  </user-provider>
</template>

<script>
import getYear from 'date-fns/get_year';

import UserProvider from '../../../store/user/Provider.vue';
import PaymentList from '../../../components/PaymentList.vue';

export default {
  name: 'PaymentsDetail',

  components: { PaymentList, UserProvider },

  computed: {
    lastYear() {
      return getYear(new Date()) - 1;
    },
  },
};
</script>
