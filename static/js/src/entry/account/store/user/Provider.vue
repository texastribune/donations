<script>
import mixin, { MODULE } from './mixin';

export default {
  name: `${MODULE}Provider`,

  mixins: [mixin],

  render() {
    const { [`${MODULE}Getters`]: getters } = this;

    return this.$scopedSlots.default({ [MODULE]: { ...getters } });
  },
};
</script>
