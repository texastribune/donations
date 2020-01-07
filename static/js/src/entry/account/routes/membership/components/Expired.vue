<template>
  <section class="c-detail-box">
    <div class="has-xxl-btm-marg">
      <info-list :items="data">
        <template v-slot="slotProps">
          <span
            :class="
              slotProps.item.text.toLowerCase().indexOf('expired') !== -1
                ? 'has-text-error'
                : 'has-text-gray-dark'
            "
          >
            {{ slotProps.item.text }}
          </span>
        </template>
      </info-list>
    </div>

    <user-internal-nav show-renew-membership show-donation-history />
  </section>
</template>

<script>
import InfoList from '../../../components/InfoList.vue';

export default {
  name: 'MembershipExpired',

  components: { InfoList },

  props: {
    data: {
      type: Array,
      required: true,
    },
  },
};
</script>
