<script>
import camelCase from 'camelcase';

import tokenUserMixin from './mixin';

export default {
  name: 'TokenUserProvider',

  mixins: [tokenUserMixin],

  computed: {
    camelCasedTokenUser() {
      const formatted = {};

      Object.keys(this.tokenUser).forEach(key => {
        formatted[camelCase(key)] = this.tokenUser[key];
      });

      return formatted;
    },
  },

  render() {
    const { camelCasedTokenUser, isLoggedIn } = this;

    return this.$scopedSlots.default({
      ...camelCasedTokenUser,
      isLoggedIn,
    });
  },
};
</script>
