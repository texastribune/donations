<script>
/* eslint-disable camelcase */

import tokenUserMixin from '../../store/token-user/mixin';

export default {
  name: 'TokenUserNavProvider',

  mixins: [tokenUserMixin],

  computed: {
    isLoggedIn() {
      return !!this.accessToken;
    },
  },

  render() {
    const { isLoggedIn } = this;

    return this.$scopedSlots.default({ isLoggedIn });
  },
};
</script>
