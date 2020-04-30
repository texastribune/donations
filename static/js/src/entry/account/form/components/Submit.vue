<template>
  <context-provider v-slot="{ context: { isViewingAs } }">
    <input
      type="submit"
      class="c-button c-button--s has-text-white has-bg-teal l-width-full l-display-block"
      :value="value"
      :disabled="isViewingAs"
    />
  </context-provider>
</template>

<script>
import ContextProvider from '../../store/context/Provider.vue';

export default {
  name: 'Submit',

  components: { ContextProvider },

  props: {
    value: {
      type: String,
      default: 'Submit',
    },
  },
};
</script>
