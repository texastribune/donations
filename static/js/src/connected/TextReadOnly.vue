<template>
  <input
    :value="value"
    :name="name"
    :required="required"
    :class="getCssClasses()"
    readonly
    type="text"
  >
</template>

<script>
import mapValueToElement from '../mixins/mapValueToElement';
import requiredField from '../mixins/requiredField';

export default {
  name: 'TextInput',

  mixins: [
    requiredField,
    mapValueToElement,
  ],
};
</script>
