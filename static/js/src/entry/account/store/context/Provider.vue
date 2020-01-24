<script>
import contextMixin from './mixin';

export default {
  name: 'ContextProvider',

  mixins: [contextMixin],

  render() {
    const { contextState } = this;

    return this.$scopedSlots.default({
      context: { ...contextState },
    });
  },
};
</script>
