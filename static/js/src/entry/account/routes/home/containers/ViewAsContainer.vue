<template>
  <view-as v-if="canViewAs" @getUser="getUser" @getOtherUser="getOtherUser" />
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
  },
};
</script>
