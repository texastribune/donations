<script>
import userMixin from './mixin';

export default {
  name: 'UserProvider',

  mixins: [userMixin],

  render() {
    return this.$scopedSlots.default(this.userGetters);
  },
};
</script>
