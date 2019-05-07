<template>
  <p>This is logged out.</p>
</template>

<script>
import userMixin from '../../mixins/user';

export default {
  name: 'Index',

  mixins: [userMixin],

  mounted() {
    this.clearFlag();
    this.redirectAfterLogOut();
  },
};
</script>
