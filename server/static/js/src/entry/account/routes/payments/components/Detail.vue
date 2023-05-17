<template>
  <user-provider v-slot="{ user: { pastTransactions } }">
    <div>
      <div class="has-xxl-btm-marg">
        <payment-list :payments="pastTransactions" />
      </div>

      <contact-us
        :ga-label="ga.userPortal.labels.payments"
        :display="{ size: 'xs' }"
        subject="custom%20tax%20receipt"
      >
        <template #text>
          Note: Donation history does not include event sponsorships or ticket
          purchases. To receive a {{ dates.lastYear }} tax receipt with this
          information, please contact
        </template>
      </contact-us>
    </div>
  </user-provider>
</template>

<script>
import UserProvider from '../../../store/user/Provider.vue';

import PaymentList from '../../../components/PaymentList.vue';
import ContactUs from '../../../components/ContactUsSmall.vue';

export default {
  name: 'PaymentsDetail',

  components: { ContactUs, PaymentList, UserProvider },
};
</script>
