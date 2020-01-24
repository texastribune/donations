<script>
import userMixin from './mixin';

export default {
  name: 'UserProvider',

  mixins: [userMixin],

  render() {
    const { userGetters } = this;

    return this.$scopedSlots.default({ user: { ...userGetters } });
  },
};
</script>
