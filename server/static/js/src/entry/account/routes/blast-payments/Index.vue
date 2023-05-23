<template>
  <div>
    <h1
      class="has-ump-top-padding has-ump-side-padding has-l-btm-marg t-size-xl"
    >
      The Blast Newsletter: Payment History
    </h1>

    <div class="has-ump-side-padding has-xxl-btm-marg">
      <section class="c-detail-box c-detail-box--from-l">
        <div class="has-xxxl-btm-marg"><detail /></div>
        <internal-nav />
      </section>
    </div>

    <contact-us :ga-label="ga.userPortal.labels['blast-payments']" is-blast>
      <template #text>
        To update your subscription to The Blast, contact us at
      </template>
    </contact-us>
  </div>
</template>

<script>
import routeMixin from '../mixin';

import userMixin from '../../store/user/mixin';

import ContactUs from '../../components/ContactUs.vue';
import Detail from './components/Detail.vue';
import InternalNav from './components/InternalNav.vue';

export default {
  name: 'BlastPaymentsRoute',

  components: { ContactUs, Detail, InternalNav },

  mixins: [routeMixin, userMixin],
};
</script>
