<template>
  <ul class="c-info-list-large">
    <li v-for="item in items" :key="item.key" class="c-info-list__item">
      <h3 class="t-size-s has-xxxs-btm-marg">
        <strong>{{ item.heading }}</strong>
      </h3>
      <p class="has-text-gray-dark">
        <slot name="text" :item="item"> {{ item.text }} </slot>
      </p>
    </li>
  </ul>
</template>

<script>
export default {
  name: 'InfoList',

  props: {
    items: {
      type: Array,
      required: true,
    },
  },
};
</script>
