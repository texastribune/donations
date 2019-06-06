<template>
  <p v-if="hasNeverGiven">I've never given!</p>
</template>

<script>
import userMixin from '../../../mixins/user';

export default {
  name: 'NeverGivenContainer',

  mixins: [userMixin],

  computed: {
    hasNeverGiven() {
      return this.user.never_given;
    },
  },
};
</script>
