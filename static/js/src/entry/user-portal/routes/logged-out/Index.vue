<template>
  <main><h1>You're logged out</h1></main>
</template>

<script>
import userMixin from '../../mixins/user';
import routeMixin from '../../mixins/route';

export default {
  name: 'Index',

  mixins: [userMixin, routeMixin],

  mounted() {
    this.user.clearFlag();
    this.user.redirectAfterLogOut();
  },
};
</script>
