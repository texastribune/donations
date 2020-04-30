export default function formatTransaction({
  amount,
  date,
  period,
  payment_type: paymentType,
  credit_card: card,
}) {
  const transaction = {
    amount,
    date,
    period,
  };

  if (paymentType && paymentType.toLowerCase() === 'credit card') {
    transaction.card = { brand: card.brand, last4: card.last4 };
  }

  return transaction;
}
