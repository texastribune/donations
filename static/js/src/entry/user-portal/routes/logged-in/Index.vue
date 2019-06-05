<template>
  <div>
    <nav-bar :show-route-links="false" />
    <main class="l-minimal has-bg-white-off has-xl-padding">
      <div class="t-align-center l-align-center-self l-align-center-x">
        <h1 class="has-xl-btm-marg">You're logged in.</h1>
        <p>Redirecting back to your original location &hellip;</p>
      </div>
    </main>
    <site-footer :show-route-links="false" />
  </div>
</template>

<script>
import { setFlag, redirectAfterLogIn } from '../../utils/auth-actions';
import routeMixin from '../../mixins/route';

export default {
  name: 'Index',

  mixins: [routeMixin],

  mounted() {
    setFlag();
    redirectAfterLogIn();
  },
};
</script>
