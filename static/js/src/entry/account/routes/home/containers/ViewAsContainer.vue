<template>
  <view-as v-if="canViewAs" @doViewAs="doViewAs" @undoViewAs="undoViewAs" />
</template>

<script>
import { mapActions } from 'vuex';

import ViewAs from '../components/ViewAs.vue';
import userMixin from '../mixins/user';
import contextMixin from '../../../mixins/context';
import tokenUserMixin from '../../../mixins/token-user';

export default {
  name: 'ViewAsContainer',

  components: { ViewAs },

  mixins: [contextMixin, userMixin, tokenUserMixin],

  methods: {
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
