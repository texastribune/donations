<script>
import tokenUserMixin from './mixin';

export default {
  name: 'TokenUserProvider',

  mixins: [tokenUserMixin],

  render() {
    const { isLoggedIn } = this;

    return this.$scopedSlots.default({ isLoggedIn });
  },
};
</script>
