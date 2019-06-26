<template>
  <aside
    class="c-appeal t-space-heading-m has-ump-side-padding has-white-off-bg-until-bp-l"
  >
    <h2 class="t-uppercase t-size-b has-s-btm-marg">
      <template v-if="isExpired">
        Member benefits
      </template>
      <template v-else>
        {{ level }} benefits
      </template>
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

    <ul class="t-linkstyle--underlined has-xl-btm-marg">
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
      class="c-button c-button--s has-text-white has-bg-teal l-width-full l-display-block"
      ga-on="click"
      :href="upgradeHref"
      :ga-event-category="ga.donations.category"
      :ga-event-action="ga.donations.actions['membership-intent']"
      :ga-event-label="ga.donations.labels['upgrade-contact']"
    >
      <template v-if="isExpired">
        Renew your support
      </template>
      <template v-else-if="isHighest">
        Join our giving Circles
      </template>
      <template v-else>
        Contact us to upgrade your membership
      </template>
    </a>
  </aside>
</template>

<script>
import BENEFITS from '../../../benefits';

export default {
  name: 'Appeal',

  props: {
    level: {
      type: String,
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
        member: 3,
        'informed member': 4,
        'engaged member': 5,
        'involved member': 6,
      };

      if (this.isExpired) return -1;
      return mapping[this.level];
    },

    isHighest() {
      return this.level === 'involved member';
    },

    upgradeHref() {
      if (this.isExpired) return this.donateUrl;
      if (this.isHighest) return this.circleUrl;

      return 'mailto:membership@texastribune.org?subject=Upgrade%20my%20Tribune%20membership&body=Hi!%20I%20would%20like%20to%20increase%20my%20support%20for%20The%20Texas%20Tribune.';
    },
  },
};
</script>
