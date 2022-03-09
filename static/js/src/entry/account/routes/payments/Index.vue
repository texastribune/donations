<template>
  <div class="has-ump-top-padding">
    <h1 class="has-ump-side-padding has-l-btm-marg t-size-xl">
      Your Donations
    </h1>

    <div class="has-ump-side-padding has-xxl-btm-marg">
      <section class="c-detail-box has-xxl-btm-marg">
        <div class="has-xxxl-btm-marg"><detail /></div>

        <internal-nav />
      </section>

      <div class="has-xxl-btm-marg"><circle-appeal /></div>

      <div class="has-xxl-btm-marg"><custom-appeal /></div>

      <div class="c-detail-box c-detail-box--from-l">
        <link-email :ga-label="ga.userPortal.labels.payments" />
      </div>
    </div>

    <appeal />

    <contact-us :ga-label="ga.userPortal.labels.membership" is-membership>
      <template #text>
        To update your membership status, contact us at
      </template>
    </contact-us>
  </div>
</template>

<script>
import userMixin from '../../store/user/mixin';
import routeMixin from '../mixin';

import Appeal from '../../appeals/containers/AppealContainer.vue';

import LinkEmail from '../../link-email/components/MiniForm.vue';
import CustomAppeal from '../../appeals/components/CustomAppeal.vue';
import CircleAppeal from '../../appeals/components/CircleAppeal.vue';
import ContactUs from '../../components/ContactUs.vue';
import Detail from './components/Detail.vue';
import InternalNav from './components/InternalNav.vue';

export default {
  name: 'PaymentsRoute',

  components: {
    LinkEmail,
    Appeal,
    CircleAppeal,
    CustomAppeal,
    Detail,
    InternalNav,
    ContactUs,
  },

  mixins: [routeMixin, userMixin],
};
</script>
