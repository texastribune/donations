<script>
import tokenUser from './mixin';

export default {
  name: 'TokenUserProvider',

  mixins: [tokenUser],

  render() {
    return this.$scopedSlots.default({
      tokenUser: { ...this.tokenUserGetters, ...this.tokenUserState },
    });
  },
};
</script>
