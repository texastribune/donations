<template>
  <aside
    class="c-appeal t-space-heading-m has-ump-side-padding has-white-off-bg-until-bp-l"
  >
    <h2 class="t-uppercase t-size-b has-s-btm-marg">Member benefits</h2>
    <p class="has-b-btm-marg">
      As a thank you for supporting our journalism, you receive:
    </p>
    <ul class="t-linkstyle--underlined has-xs-btm-marg">
      <li
        v-for="(benefit, index) in benefits"
        :key="benefit.id"
        :aria-label="
          index > ceiling ? 'benefit not achieved' : 'benefit achieved'
        "
        :class="{
          'has-xs-btm-marg': index !== benefits.length - 1,
          'c-appeal__item--no': index >= ceiling,
        }"
        class="c-appeal__item"
      >
        <icon :name="index < ceiling ? 'camera' : 'camera'" />
        <component :is="benefit.component" />
      </li>
    </ul>
    <a
      class="c-button c-button--s has-text-white has-bg-teal l-width-full l-display-block"
      href="mailto:community@texastribune.org"
      >Contact us for more membership information</a
    >
  </aside>
</template>

<script>
import BENEFITS from '../benefits';

export default {
  name: 'Appeal',

  props: {
    level: {
      type: String,
      default: 'informed',
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
        member: 0,
        informed: 5,
        engaged: 6,
        involved: 7,
        editors: 7,
        chairman: 7,
        leadership: 7,
      };

      return mapping[this.level];
    },
  },
};
</script>
