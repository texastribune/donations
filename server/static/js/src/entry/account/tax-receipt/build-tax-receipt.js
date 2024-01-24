import format from 'date-fns/format';
import jsPDF from 'jspdf';
import axios from 'axios';

import formatCurrency from '../utils/format-currency';

export default async function buildTaxReceipt({
  lastYear,
  lastYearAmount,
  greeting,
}) {
  // eslint-disable-next-line new-cap
  const doc = new jsPDF({
    unit: 'px',
    format: 'letter',
    lineHeight: 1.5,
  });
  doc.setFont('helvetica');

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
      'P: 512-993-0166',
      'www.texastribune.org',
    ],
    425,
    topEdge,
    { align: 'right' }
  );

  doc.setFontSize(12);
  doc.text(`${format(new Date(), 'MMMM D, YYYY')}`, leftEdge, 130);
  doc.text(`Dear ${greeting || 'Donor'},`, leftEdge, 155);
  doc.text(
    `Thank you for your support of The Texas Tribune — the only nonpartisan, member-supported, digitally focused news organization that covers Texas public policy, politics, government and statewide issues. Our nonprofit newsroom relies on the generosity of people like you, which is why your support helps us produce serious journalism about issues that matter to Texas. Please find your ${lastYear} giving summary below.`,
    leftEdge,
    180,
    { maxWidth: '385' }
  );

  doc.setFont('helvetica', 'bold');
  doc.text(`${lastYear} GIVING SUMMARY`, leftEdge, 265);

  if (greeting) {
    doc.text('Donor', leftEdge, 290);
    doc.setFont('helvetica', 'normal');
    doc.text(greeting, leftEdge, 302);

    doc.setFont('helvetica', 'bold');
    doc.text('Total donation amount', leftEdge, 327);
    doc.setFont('helvetica', 'normal');
    doc.text(formatCurrency(lastYearAmount), leftEdge, 340);

    doc.text(
      "Thanks so much. We couldn't do this work without you!",
      leftEdge,
      365
    );

    doc.text('The Texas Tribune Team', leftEdge, 390);
    doc.text(
      'Questions: membership@texastribune.org / 512.716.8695',
      leftEdge,
      402
    );

    doc.text(
      'No goods or services were provided in exchange for this contribution. This letter may be used as a receipt for tax purposes. The Texas Tribune is a 501(c)3 nonprofit organization with Federal Tax ID #26-4527097.',
      leftEdge,
      427,
      { maxWidth: '385' }
    );
  } else {
    // have to repeat some logic because different spacing
    // is required if greeting is missing

    doc.setFont('helvetica', 'bold');
    doc.text('Total donation amount', leftEdge, 290);
    doc.setFont('helvetica', 'normal');
    doc.text(formatCurrency(lastYearAmount), leftEdge, 302);

    doc.text(
      "Thanks so much. We couldn't do this work without you!",
      leftEdge,
      327
    );

    doc.text('The Texas Tribune Team', leftEdge, 352);
    doc.text(
      'Questions: membership@texastribune.org / 512.716.8695',
      leftEdge,
      364
    );

    doc.text(
      'No goods or services were provided in exchange for this contribution. This letter may be used as a receipt for tax purposes. The Texas Tribune is a 501(c)3 nonprofit organization with Federal Tax ID #26-4527097.',
      leftEdge,
      389,
      { maxWidth: '385' }
    );
  }

  doc.save(`${lastYear}-texas-tribune-tax-receipt.pdf`);
}
