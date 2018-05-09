<template>
  <input
    :value="value"
    :name="name"
    :required="required"
    :placeholder="placeholder"
    :class="getCssClasses()"
    type="email"
    @input="onInput($event.target.value)"
  >
</template>

<script>
import mapValueToElement from '../mixins/mapValueToElement';
import replaceSingleValueOnInput from '../mixins/replaceSingleValueOnInput';
import requiredField from '../mixins/requiredField';
import fieldWithPlaceholder from '../mixins/fieldWithPlaceholder';

export default {
  name: 'Email',

  mixins: [
    requiredField,
    mapValueToElement,
    fieldWithPlaceholder,
    replaceSingleValueOnInput,
  ],
};
</script>
