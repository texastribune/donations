<script>
import mixin, { MODULE } from './mixin';

export default {
  name: `${MODULE}Provider`,

  mixins: [mixin],

  render() {
    const { [`${MODULE}State`]: state, [`${MODULE}Getters`]: getters } = this;

    return this.$scopedSlots.default({
      [MODULE]: { ...state, ...getters },
    });
  },
};
</script>
