<template>
  <route-loader v-if="routeIsFetching">
    <template v-slot:text>
      Grabbing your Blast information
    </template>
  </route-loader>

  <div v-else class="has-ump-top-padding">
    <message :ga-close-label="ga.userPortal.labels.blast" />

    <h1 class="has-xl-btm-marg has-ump-side-padding t-size-xl">
      The Blast Newsletter
    </h1>

    <div class="has-ump-side-padding has-xl-btm-marg"><detail /></div>

    <help blast />
  </div>
</template>

<script>
/* eslint-disable camelcase */

import routeMixin from '../../mixins/route';
import userMixin from '../../store/user/mixin';
import RouteLoader from '../home/components/RouteLoader.vue';
import Help from '../home/components/Help.vue';
import Message from '../home/containers/MessageContainer.vue';
import Detail from './containers/DetailContainer.vue';
import { InvalidRouteError } from '../../errors';

export default {
  name: 'BlastRoute',

  components: { Help, Detail, RouteLoader, Message },

  mixins: [routeMixin, userMixin],

  data() {
    return { title: 'The Blast' };
  },

  methods: {
    async fetchData() {
      const meetsCriteria = this.user.is_blast_subscriber;
      if (!meetsCriteria) throw new InvalidRouteError();
    },
  },
};
</script>
