<template>
  <route-loader v-if="routeIsFetching">
    <template v-slot:text>
      Grabbing your Blast information
    </template>
  </route-loader>

  <div v-else>
    <h1
      class="has-ump-top-padding has-xl-btm-marg has-ump-side-padding t-size-xl"
    >
      The Blast Newsletter
    </h1>

    <div class="has-ump-side-padding has-xl-btm-marg">
      <section class="c-detail-box c-detail-box--from-l">
        <div class="has-xxxl-btm-marg"><detail /></div>

        <internal-nav />
      </section>
    </div>

    <help blast />
  </div>
</template>

<script>
/* eslint-disable camelcase */

import routeMixin from '../mixin';
import userMixin from '../../store/user/mixin';
import RouteLoader from '../home/components/RouteLoader.vue';
import Help from '../home/components/Help.vue';
import Detail from './containers/DetailContainer.vue';
import InternalNav from './components/InternalNav.vue';
import { InvalidRouteError } from '../../errors';

export default {
  name: 'BlastRoute',

  components: { Help, Detail, RouteLoader, InternalNav },

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
