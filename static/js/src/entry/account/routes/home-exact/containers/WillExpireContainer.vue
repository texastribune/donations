<template>
  <transition name="has-fade"> <will-expire v-if="shouldShow" /> </transition>
</template>

<script>
/* eslint-disable camelcase */

import userMixin from '../../home/mixins/user';
import { CARD_PAYMENT_FLAG } from '../../../constants';

const WillExpire = () =>
  import(/* webpackChunkName: "will-expire-summary" */ '../components/WillExpire.vue');

export default {
  name: 'WillExpireContainer',

  components: { WillExpire },

  mixins: [userMixin],

  computed: {
    shouldShow() {
      const {
        is_recurring_donor,
        is_circle_donor,
        is_expired,
        will_expire,
      } = this.user;

      return (is_recurring_donor || is_circle_donor) && will_expire;
    },
  },
};
</script>
