<template>
  <li class="c-link-list__item">
    <span class="c-link-list__arrow has-text-teal">
      <strong>&rarr;</strong>
    </span>
    <span class="has-text-gray-dark"> <slot></slot> </span>
  </li>
</template>

<script>
// ordering
// differing text
// !!accessToken
// component names
// maybe: internal --> inline
// check summary-box--from-l
// removal of props

export default {
  name: 'InternalNavItem',
};
</script>
