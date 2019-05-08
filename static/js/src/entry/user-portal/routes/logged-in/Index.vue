<template>
  <main>
    <h1>You're logged in</h1>
    <p>Redirecting you back to your original location.</p>
  </main>
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
