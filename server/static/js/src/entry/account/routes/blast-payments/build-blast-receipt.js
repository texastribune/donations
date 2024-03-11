import jsPDF from 'jspdf';
import axios from 'axios';

import formatCurrency from '../../utils/format-currency';
import formatShortDate from '../../utils/format-short-date';

export default async function buildBlastReceipt({ date, amount, card }) {
  // eslint-disable-next-line new-cap
  const doc = new jsPDF({
    unit: 'px',
    format: 'letter',
    lineHeight: 1.5,
  });
  doc.setFont('helvetica');

  const formattedDate = formatShortDate(date);
  const leftEdge = 40;
  const topEdge = 30;
  const response = await axios.get('/static/img/receipt-logo.png', {
    responseType: 'blob',
  });
  const ttLogo = await new Promise((resolve, reject) => {
    const reader = new window.FileReader();

    reader.readAsDataURL(response.data);
    reader.onerror = reject;
    reader.onload = () => {
      resolve(reader.result);
    };
  });

  doc.addImage(ttLogo, 'PNG', leftEdge, topEdge, 100, 50);

  doc.setFontSize(10);
  doc.text(
    [
      '919 Congress Avenue, Sixth Floor',
      'Austin, TX 78701',
      'P: 512-716-8600',
      'F: 512-716-8601',
      'www.texastribune.org',
    ],
    425,
    topEdge,
    { align: 'right' }
  );

  doc.setFontSize(12);
  doc.text('Thank you for subscribing to The Blast!', leftEdge, 130);

  doc.setFont('helvetica', 'bold');
  doc.text('Date', leftEdge, 160);
  doc.setFont('helvetica', 'normal');
  doc.text(formattedDate, leftEdge, 172);

  doc.setFont('helvetica', 'bold');
  doc.text('Amount', leftEdge, 202);
  doc.setFont('helvetica', 'normal');
  doc.text(formatCurrency(amount), leftEdge, 214);

  if (card) {
    doc.setFont('helvetica', 'bold');
    doc.text('Payment method', leftEdge, 244);
    doc.setFont('helvetica', 'normal');
    doc.text(`${card.brand} ${card.last4}`, leftEdge, 256);
    doc.text(
      'If you have any questions, email us at blast@texastribune.org or call 512-993-0166.',
      leftEdge,
      286,
      { maxWidth: '385' }
    );
  } else {
    doc.text(
      'If you have any questions, email us at blast@texastribune.org or call 512-993-0166.',
      leftEdge,
      244,
      { maxWidth: '385' }
    );
  }

  doc.save(`blast-receipt-${formattedDate}.pdf`);
}
