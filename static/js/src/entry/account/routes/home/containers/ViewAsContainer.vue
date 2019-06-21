<template>
  <view-as v-if="canViewAs" @doViewAs="doViewAs" @undoViewAs="undoViewAs" />
</template>

<script>
import { mapActions, mapState } from 'vuex';

import ViewAs from '../components/ViewAs.vue';

export default {
  name: 'ViewAsContainer',

  components: { ViewAs },

  computed: {
    ...mapState('user', ['canViewAs']),
  },

  methods: {
    ...mapActions('user', ['getUser', 'getOtherUser']),

    ...mapActions('context', ['setIsViewingAs']),

    async doViewAs(email) {
      await this.getOtherUser(email);
      this.setIsViewingAs(true);
    },

    async undoViewAs(cb) {
      await this.getUser();
      this.setIsViewingAs(false);
      cb();
    },
  },
};
</script>
