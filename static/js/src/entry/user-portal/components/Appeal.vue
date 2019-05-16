<template>
  <aside
    class="c-appeal t-space-heading-m t-linkstyle--underlined has-ump-side-padding has-ump-top-padding-until-bp-l has-xxl-btm-marg-from-bp-l has-white-off-bg-until-bp-l"
  >
    <h2 class="t-uppercase t-size-m has-s-btm-marg">Member benefits</h2>
    <p class="has-b-btm-marg">
      As a thank you for supporting our journalism, you receive:
    </p>
    <ul>
      <li
        v-for="(benefit, index) in benefits"
        :key="benefit.id"
        :aria-label="
          index > ceiling ? 'benefit not achieved' : 'benefit achieved'
        "
        :class="{
          'has-xs-btm-marg': index !== benefits.length - 1,
          'c-appeal__item--no': index > ceiling,
        }"
        class="c-appeal__item"
      >
        <icon :name="index <= ceiling ? 'camera' : 'close'" />
        <component :is="benefit.component" />
      </li>
    </ul>
  </aside>
</template>

<script>
import BENEFITS from '../benefits';
import Icon from './Icon.vue';

export default {
  name: 'Appeal',

  components: { Icon },

  props: {
    ceiling: {
      type: Number,
      default: 3,
    },
  },

  data() {
    return {
      benefits: BENEFITS,
    };
  },
};
</script>
