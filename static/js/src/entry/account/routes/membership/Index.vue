<template>
  <div class="has-ump-top-padding">
    <credit-card-message :ga-label="ga.userPortal.labels.membership" />

    <h1 class="has-ump-side-padding has-xl-btm-marg t-size-xl">
      Your Membership
    </h1>

    <div class="has-ump-side-padding has-xxl-btm-marg">
      <div class="has-xxl-btm-marg">
        <expired />
        <recurring-or-circle />
        <single-or-will-expire />
      </div>

      <div class="has-xxl-btm-marg"><circle-appeal /></div>

      <div class="c-detail-box c-detail-box--from-l">
        <link-email :ga-label="ga.userPortal.labels.membership" />
      </div>
    </div>

    <appeal />

    <contact-us :ga-label="ga.userPortal.labels.membership" is-membership>
      <template v-slot:text>
        To update your membership status, contact us at
      </template>
    </contact-us>
  </div>
</template>

<script>
import ContactUs from '../../components/ContactUs.vue';
import userMixin from '../../store/user/mixin';
import LinkEmail from '../../link-email/components/LinkEmail.vue';
import CircleAppeal from '../../appeals/components/CircleAppeal.vue';
import Appeal from '../../appeals/containers/AppealContainer.vue';
import CreditCardMessage from '../../messages/components/CreditCardMessage.vue';
import routeMixin from '../mixin';
import Expired from './containers/ExpiredContainer.vue';
import RecurringOrCircle from './containers/RecurringOrCircleContainer.vue';
import SingleOrWillExpire from './containers/SingleOrWillExpireContainer.vue';

export default {
  name: 'MembershipRoute',

  components: {
    Expired,
    RecurringOrCircle,
    SingleOrWillExpire,
    Appeal,
    CreditCardMessage,
    CircleAppeal,
    ContactUs,
    LinkEmail,
  },

  mixins: [routeMixin, userMixin],
};
</script>
