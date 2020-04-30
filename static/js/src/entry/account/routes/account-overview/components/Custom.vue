<template>
  <summary-box heading="membership">
    <template v-slot:content>
      <p class="has-text-gray-dark">
        Thank you for being a Texas Tribune member!
      </p>
    </template>

    <template v-slot:links>
      <user-internal-nav show-donation-history />
    </template>
  </summary-box>
</template>

<script>
import SummaryBox from '../../../components/SummaryBox.vue';

export default {
  name: 'SummaryCustom',

  components: { SummaryBox },
};
</script>
