<template>
  <li class="c-link-list__item">
    <div :class="extraSlotExists && 'has-xxxs-btm-marg'">
      <span class="c-link-list__arrow has-text-teal">
        <strong>&rarr;</strong>
      </span>
      <span class="has-text-gray-dark"> <slot name="main"></slot> </span>
    </div>
    <slot name="extra"></slot>
  </li>
</template>

<script>
export default {
  name: 'LinkListItem',

  computed: {
    extraSlotExists() {
      return !!this.$slots.extra;
    },
  },
};
</script>
