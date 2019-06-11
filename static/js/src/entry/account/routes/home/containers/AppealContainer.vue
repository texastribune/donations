<template>
  <appeal :level="user.membership_level" />
</template>

<script>
import Appeal from '../components/Appeal.vue';
import userMixin from '../mixins/user';

export default {
  name: 'AppealContainer',

  components: { Appeal },

  mixins: [userMixin],
};
</script>
