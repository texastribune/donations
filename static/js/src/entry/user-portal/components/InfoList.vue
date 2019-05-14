<template>
  <ul class="c-info-list">
    <li v-for="item in items" :key="item.id" class="c-info-list__item">
      <h3 class="t-size-s has-xxxs-btm-marg">
        <strong>{{ item.heading }}</strong>
      </h3>
      <p>
        <slot :item="item">
          <span class="has-text-gray-dark">{{ item.text }}</span>
        </slot>
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
