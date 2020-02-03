<script>
import mixin, { MODULE } from './mixin';

export default {
  name: `${MODULE}Provider`,

  mixins: [mixin],

  render() {
    const { [`${MODULE}Getters`]: getters, [`${MODULE}State`]: state } = this;

    return this.$scopedSlots.default({
      [MODULE]: { ...getters, ...state },
    });
  },
};
</script>
