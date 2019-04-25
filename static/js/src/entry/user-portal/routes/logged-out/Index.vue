<template>
  <p>This is logged out.</p>
</template>

<script>
import userMixin from '../../mixins/user';

export default {
  name: 'Index',

  mixins: [userMixin],

  mounted() {
    this.user.clearFlag();
    this.user.redirectAfterLogOut();
  },
};
</script>
