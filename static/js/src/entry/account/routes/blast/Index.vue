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
      <current /> <former />
    </div>

    <help blast />
  </div>
</template>

<script>
import routeMixin from '../mixin';
import userMixin from '../../store/user/mixin';
import { InvalidRouteError } from '../../errors';
import RouteLoader from '../home/components/RouteLoader.vue';
import Current from './containers/CurrentContainer.vue';
import Former from './containers/FormerContainer.vue';
import Help from '../home/components/Help.vue';

export default {
  name: 'BlastRoute',

  components: { Help, Current, Former, RouteLoader },

  mixins: [routeMixin, userMixin],

  data() {
    return { title: 'The Blast' };
  },

  methods: {
    async fetchData() {
      const meetsCriteria = this.user.isBlastSubscriber;
      if (!meetsCriteria) throw new InvalidRouteError();
    },
  },
};
</script>
