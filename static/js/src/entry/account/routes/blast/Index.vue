<template>
  <div v-if="!routeIsFetching" class="has-ump-top-padding">
    <h1 class="has-xl-btm-marg has-ump-side-padding t-size-xl">
      The Blast Newsletter
    </h1>

    <div class="has-ump-side-padding has-xl-btm-marg"><blast-detail /></div>

    <help blast :display="{ hasTopPadding: true }" />
  </div>
</template>

<script>
/* eslint-disable camelcase */

import routeMixin from '../../mixins/route';
import userMixin from '../home/mixins/user';
import Help from '../../components/Help.vue';
import BlastDetail from './containers/BlastDetailContainer.vue';
import { InvalidRouteError } from '../../errors';

export default {
  name: 'BlastRoute',

  components: { Help, BlastDetail },

  mixins: [routeMixin, userMixin],

  computed: {
    route() {
      return {
        isExact: true,
        isProtected: false,
        title: 'The Blast',
      };
    },
  },

  methods: {
    async fetchData() {
      const {
        is_former_blast_subscriber,
        is_current_blast_subscriber,
      } = this.user;
      const meetsCriteria =
        is_former_blast_subscriber || is_current_blast_subscriber;

      if (!meetsCriteria) throw new InvalidRouteError();
    },
  },
};
</script>
