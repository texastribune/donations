<template>
  <li class="c-link-list__item">
    <span class="c-link-list__arrow has-text-teal">
      <strong>&rarr;</strong>
    </span>
    <span class="has-text-gray-dark"> <slot></slot> </span>
  </li>
</template>

<script>
// differing text
// component names
// check summary-box--from-l
// removal of props

export default {
  name: 'InternalNavItem',
};
</script>
