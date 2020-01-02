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
    return this.$scopedSlots.default(this.camelCasedTokenUser);
  },
};
</script>
