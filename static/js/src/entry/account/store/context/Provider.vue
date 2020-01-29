<script>
import mixin, { MODULE } from './mixin';

export default {
  name: `${MODULE}Provider`,

  mixins: [mixin],

  render() {
    const { [`${MODULE}State`]: state } = this;

    return this.$scopedSlots.default({
      [MODULE]: { ...state },
    });
  },
};
</script>
