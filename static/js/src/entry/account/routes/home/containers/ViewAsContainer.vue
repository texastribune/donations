<template>
  <view-as v-if="canViewAs" @doViewAs="doViewAs" @undoViewAs="undoViewAs" />
</template>

<script>
import { mapActions } from 'vuex';

import ViewAs from '../components/ViewAs.vue';
import userMixin from '../../../store/user/mixin';
import tokenUserMixin from '../../../store/token-user/mixin';
import contextMixin from '../../../store/context/mixin';

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

    async undoViewAs() {
      this.setAppIsFetching(true);

      await this.getUser();

      this.setIsViewingAs(false);
      this.setAppIsFetching(false);
    },
  },
};
</script>
