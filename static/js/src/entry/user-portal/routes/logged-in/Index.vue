<template>
  <p>This is logged in.</p>
</template>

<script>
import userMixin from '../../mixins/user';

export default {
  name: 'Index',

  mixins: [userMixin],

  mounted() {
    this.setFlag();
    this.redirectAfterLogIn();
  },
};
</script>
