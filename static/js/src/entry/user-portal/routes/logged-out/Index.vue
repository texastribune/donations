<template>
  <p>This is logged out.</p>
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
