<template>
  <route-loader v-if="routeIsFetching">
    <template v-slot:text>
      Grabbing your Blast payment history
    </template>
  </route-loader>

  <div v-else>
    <h1
      class="has-ump-top-padding has-ump-side-padding has-l-btm-marg t-size-xl"
    >
      The Blast Newsletter: Payment History
    </h1>

    <div class="has-ump-side-padding has-xxl-btm-marg"><detail /></div>

    <help blast-payments />
  </div>
</template>

<script>
/* eslint-disable camelcase */

import routeMixin from '../mixin';
import userMixin from '../../store/user/mixin';
import Help from '../home/components/Help.vue';
import RouteLoader from '../home/components/RouteLoader.vue';
import Detail from './containers/DetailContainer.vue';
import { InvalidRouteError } from '../../errors';

export default {
  name: 'BlastPaymentsRoute',

  components: { Help, Detail, RouteLoader },

  mixins: [routeMixin, userMixin],

  data() {
    return { title: 'The Blast Payment History' };
  },

  methods: {
    async fetchData() {
      const meetsCriteria = this.user.is_blast_subscriber;

      if (!meetsCriteria) throw new InvalidRouteError();
    },
  },
};
</script>
