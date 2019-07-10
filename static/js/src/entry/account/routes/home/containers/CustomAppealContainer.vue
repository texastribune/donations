<template>
  <custom-appeal v-if="shouldShow" />
</template>

<script>
/* eslint-disable camelcase */

import CustomAppeal from '../components/CustomAppeal.vue';
import userMixin from '../mixins/user';

export default {
  name: 'CustomAppealContainer',

  components: { CustomAppeal },

  mixins: [userMixin],

  computed: {
    shouldShow() {
      return this.user.is_custom_donor;
    },
  },
};
</script>
