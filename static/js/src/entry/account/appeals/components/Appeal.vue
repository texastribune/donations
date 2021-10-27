<template>
  <aside
    class="c-appeal t-lh-b has-ump-side-padding has-white-off-bg-until-bp-l"
  >
    <h2 class="t-uppercase t-size-b has-s-btm-marg">
      <template v-if="isExpired"> Member benefits </template>
      <template v-else> {{ membershipLevel }} benefits </template>
    </h2>

    <p class="has-b-btm-marg">
      <template v-if="isExpired">
        In addition to the happiness that comes with supporting mission-driven
        journalism, we like to give our members a little something extra as
        tokens of our appreciation. Renew your membership now and you’ll be
        eligible to receive:
      </template>
      <template v-else>
        As a thank you for supporting our journalism, you receive:
      </template>
    </p>

    <ul class="t-links-underlined has-xl-btm-marg">
      <li
        v-for="(benefit, index) in benefits"
        :key="benefit.id"
        :aria-hidden="index > ceiling"
        :class="{
          'has-xs-btm-marg': index !== benefits.length - 1,
          'c-appeal__item--no': index > ceiling,
        }"
        class="c-appeal__item"
      >
        <icon :name="index > ceiling ? 'close' : 'check'" />
        <component :is="benefit.component" />
      </li>
    </ul>

    <p v-if="!isExpired" class="has-xs-btm-marg">
      <strong>Ready to take your giving to the next level?</strong>
    </p>

    <a
      class="
        c-button c-button--s
        has-text-white has-bg-teal
        l-width-full l-display-block
      "
      ga-on="click"
      :href="upgradeHref"
      :ga-event-category="ga.donations.category"
      :ga-event-action="ga.donations.actions['membership-intent']"
      :ga-event-label="ga.donations.labels['upgrade-contact']"
    >
      <template v-if="isExpired"> Renew your support </template>
      <template v-else-if="isHighest"> Join our giving Circles </template>
      <template v-else> Contact us to upgrade your membership </template>
    </a>
  </aside>
</template>

<script>
import BENEFITS from './benefits';

export default {
  name: 'Appeal',

  props: {
    membershipLevel: {
      validator: (value) => typeof value === 'string' || value === null,
      required: true,
    },

    isExpired: {
      type: Boolean,
      required: true,
    },
  },

  data() {
    return {
      benefits: BENEFITS,
    };
  },

  computed: {
    ceiling() {
      const mapping = {
        member: 2,
        'informed member': 3,
        'engaged member': 4,
        'involved member': 5,
      };

      if (this.isExpired) {
        return -1;
      }
      return mapping[this.membershipLevel];
    },

    isHighest() {
      return this.membershipLevel === 'involved member';
    },

    upgradeHref() {
      if (this.isExpired) {
        return this.urls.donate;
      }
      if (this.isHighest) {
        return this.urls.circle;
      }

      return 'mailto:membership@texastribune.org?subject=Upgrade%20my%20Tribune%20membership&body=Hi!%20I%20would%20like%20to%20increase%20my%20support%20for%20The%20Texas%20Tribune.';
    },
  },
};
</script>
