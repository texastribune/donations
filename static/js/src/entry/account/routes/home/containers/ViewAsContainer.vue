<template>
  <view-as v-if="canViewAs" @doViewAs="doViewAs" @undoViewAs="undoViewAs" />
</template>

<script>
import { mapActions, mapState } from 'vuex';

import ViewAs from '../components/ViewAs.vue';
import contextMixin from '../../../mixins/context';

export default {
  name: 'ViewAsContainer',

  components: { ViewAs },

  mixins: [contextMixin],

  computed: {
    ...mapState('tokenUser', ['canViewAs']),
  },

  methods: {
    ...mapActions('user', ['getUser', 'getOtherUser']),

    ...mapActions('context', ['setIsViewingAs']),

    async doViewAs(email) {
      this.setAppIsFetching(true);

      await this.getOtherUser(email);

      this.setIsViewingAs(true);
      this.setAppIsFetching(false);
    },

    async undoViewAs(cb) {
      this.setAppIsFetching(true);

      await this.getUser();

      this.setIsViewingAs(false);
      this.setAppIsFetching(false);
      cb();
    },
  },
};
</script>
