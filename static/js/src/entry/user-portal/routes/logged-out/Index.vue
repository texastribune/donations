<template>
  <div>
    <main class="l-minimal has-bg-white-off has-xl-padding">
      <div class="t-align-center l-align-center-self l-align-center-x">
        <h1 class="has-xl-btm-marg">You're logged out.</h1>
        <p>Redirecting you to texastribune.org &hellip;</p>
      </div>
    </main>
    <site-footer />
  </div>
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
