<template>
  <summary-box heading="profile settings">
    <template v-slot:content>
      <info-list :items="contactInfo">
        <template v-slot="slotProps">
          <span
            class="has-text-gray-dark"
            :class="{ 't-wrap-break': slotProps.item.heading === 'Email' }"
          >
            {{ slotProps.item.text }}
          </span>
        </template>
      </info-list>
    </template>

    <template v-slot:links>
      <user-internal-nav
        show-edit-profile
        show-reset-pw
        :pw-reset-ga-label="ga.userPortal.labels.home"
      />
    </template>
  </summary-box>
</template>

<script>
import SummaryBox from '../../../components/SummaryBox.vue';
import InfoList from '../../../components/InfoList.vue';

export default {
  name: 'SummaryProfileSettings',

  components: { SummaryBox, InfoList },

  props: {
    contactInfo: {
      type: Array,
      required: true,
    },
  },
};
</script>
