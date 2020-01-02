<script>
import camelCase from 'camelcase';

import userMixin from './mixin';

export default {
  name: 'UserProvider',

  mixins: [userMixin],

  computed: {
    camelCasedUser() {
      const formatted = {};

      Object.keys(this.user).forEach(key => {
        formatted[camelCase(key)] = this.user[key];
      });

      return formatted;
    },
  },

  render() {
    return this.$scopedSlots.default(this.camelCasedUser);
  },
};
</script>
