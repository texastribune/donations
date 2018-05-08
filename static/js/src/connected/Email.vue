<template>
  <input
    :value="value"
    :name="name"
    :required="required"
    type="email"
    @input="onInput($event.target.value)"
  >
</template>

<script>
import mapValueToElement from '../mixins/mapValueToElement';
import replaceSingleValueOnInput from '../mixins/replaceSingleValueOnInput';
import requiredField from '../mixins/requiredField';

export default {
  name: 'Email',

  mixins: [
    requiredField,
    mapValueToElement,
    replaceSingleValueOnInput,
  ],
};
</script>
