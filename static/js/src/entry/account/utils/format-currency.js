export default function formatCurrency(value) {
  const hasDecimal = value.toString().indexOf('.') !== -1;

  if (hasDecimal) {
    const withZeroes = value.toFixed(2);
    const withCommas = withZeroes.replace(/\B(?=(\d{3})+(?!\d))/g, ',');

    return `$${withCommas}`;
  }

  const withCommas = value.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');

  return `$${withCommas}`;
}
