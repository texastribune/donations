<template>
  <p>This is logged in.</p>
</template>

<script>
import userMixin from '../../mixins/user';
import routeMixin from '../../mixins/route';

export default {
  name: 'Index',

  mixins: [userMixin, routeMixin],

  mounted() {
    this.user.setFlag();
    this.user.redirectAfterLogIn();
  },
};
</script>
