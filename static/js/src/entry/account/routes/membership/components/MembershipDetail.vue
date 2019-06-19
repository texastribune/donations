<template>
  <section class="c-detail-box">
    <div class="has-xxl-btm-marg">
      <info-list :items="data">
        <template v-slot="slotProps">
          <span
            :class="
              slotProps.item.text.toLowerCase() === 'your membership expired.'
                ? 'has-text-error'
                : 'has-text-gray-dark'
            "
          >
            <template
              v-if="slotProps.item.heading.toLowerCase() === 'last donation'"
            >
              {{ slotProps.item.text | amountAndDate }}
            </template>
            <template
              v-else-if="slotProps.item.heading.toLowerCase() === 'donation'"
            >
              {{ slotProps.item.text | amountAndPeriod }}
            </template>
            <template
              v-else-if="
                slotProps.item.heading.toLowerCase() === 'next payment'
              "
            >
              {{ slotProps.item.text | longDate }}
            </template>
            <template v-else>
              {{ slotProps.item.text }}
            </template>
          </span>
        </template>
      </info-list>
    </div>

    <ul class="c-link-list t-linkstyle--underlined">
      <li v-if="isExpired && !isOneTime" class="has-xs-btm-marg">
        <span class="c-link-list__arrow has-text-teal">
          <strong>&rarr;</strong>
        </span>
        <span class="has-text-gray-dark">
          <a
            href="#"
            ga-on="click"
            :ga-event-category="ga.donations.category"
            :ga-event-action="ga.donations.actions['membership-intent']"
            :ga-event-label="ga.donations.labels['renew-membership']"
          >
            Renew your membership
          </a>
        </span>
      </li>
      <li v-if="isOneTime" class="has-xs-btm-marg">
        <span class="c-link-list__arrow has-text-teal">
          <strong>&rarr;</strong>
        </span>
        <span class="has-text-gray-dark">
          <a
            href="#"
            ga-on="click"
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
import formatCurrency from '../../../utils/format-currency';
import formatLongDate from '../../../utils/format-long-date';

export default {
  name: 'MembershipDetail',

  components: { InfoList },

  filters: {
    amountAndPeriod(value) {
      const [amount, period] = value.split('|');
      return `${formatCurrency(parseFloat(amount))}, ${period}`;
    },

    amountAndDate(value) {
      const [amount, date] = value.split('|');
      return `${formatCurrency(parseFloat(amount))}, ${formatLongDate(date)}`;
    },
  },

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
  },
};
</script>
