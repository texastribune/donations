<template>
  <div v-if="route.meetsCriteria" class="has-bg-white has-ump-top-padding">
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

export default {
  name: 'BlastRoute',

  components: { Help, BlastDetail },

  mixins: [routeMixin, userMixin],

  computed: {
    route() {
      const {
        is_former_blast_subscriber,
        is_current_blast_subscriber,
      } = this.user;
      const meetsCriteria =
        is_former_blast_subscriber || is_current_blast_subscriber;

      return {
        isExact: true,
        isProtected: false,
        meetsCriteria,
        title: 'The Blast',
      };
    },
  },

  methods: {
    async fetchData() {
      // await this.getUser();
      this.$router.push({ name: 'membership' });
    },
  },
};
</script>
