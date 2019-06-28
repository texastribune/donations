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

    <ul class="c-link-list t-linkstyle--underlined">
      <li v-if="isExpired" class="has-xs-btm-marg">
        <span class="c-link-list__arrow has-text-teal">
          <strong>&rarr;</strong>
        </span>
        <span class="has-text-gray-dark">
          <a
            :href="isFormerCircle ? circleUrl : donateUrl"
            ga-on="click"
            :ga-event-category="ga.donations.category"
            :ga-event-action="ga.donations.actions['membership-intent']"
            :ga-event-label="ga.donations.labels['renew-membership']"
          >
            Renew your membership
          </a>
        </span>
      </li>
      <li v-else-if="isOneTime" class="has-xs-btm-marg">
        <span class="c-link-list__arrow has-text-teal">
          <strong>&rarr;</strong>
        </span>
        <span class="has-text-gray-dark">
          <a
            ga-on="click"
            :href="donateUrl"
            :ga-event-category="ga.donations.category"
            :ga-event-action="ga.donations.actions['membership-intent']"
            :ga-event-label="ga.donations.labels['upgrade-membership']"
          >
            Become a sustaining member
          </a>
        </span>
      </li>
      <li>
        <span class="c-link-list__arrow has-text-teal">
          <strong>&rarr;</strong>
        </span>
        <span class="has-text-gray-dark">
          <router-link
            ga-on="click"
            :to="{ name: 'payments' }"
            :ga-event-category="ga.userPortalNav.category"
            :ga-event-action="ga.userPortalNav.actions.inline"
            :ga-event-label="ga.userPortalNav.labels.payments"
          >
            See your donation history
          </router-link>
        </span>
      </li>
    </ul>
  </section>
</template>

<script>
import InfoList from '../../../components/InfoList.vue';

export default {
  name: 'MembershipDetail',

  components: { InfoList },

  props: {
    data: {
      type: Array,
      required: true,
    },

    isExpired: {
      type: Boolean,
      required: true,
    },

    isOneTime: {
      type: Boolean,
      required: true,
    },

    isFormerCircle: {
      type: Boolean,
      required: true,
    },
  },
};
</script>
