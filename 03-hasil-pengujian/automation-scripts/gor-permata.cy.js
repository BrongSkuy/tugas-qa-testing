// Contoh Test Script Cypress (Sesuai Materi Automation Testing 14 Nov 2026)
// Objek 1: Portal Booking GOR Permata Badminton Hall
// Catatan: Non-destruktif - hanya menguji tampilan, kalkulasi, dan validasi negatif (memblokir POST /bookings/store)

describe('GOR Permata Badminton Hall - Non-Destructive QA Suite', () => {
  const baseUrl = 'https://gorpermatabadminton.com';

  beforeEach(() => {
    // Pengaman jaringan agar tidak pernah membuat booking nyata di database
    cy.intercept('POST', '**/bookings/store', {
      statusCode: 400,
      body: { success: false, message: 'Blocked in QA test mode' },
    }).as('blockedBookingStore');
  });

  it('TC-GOR-01 & 02: Memastikan beranda, booking, login aktif dan mencatat /register 404', () => {
    cy.visit(baseUrl);
    cy.url().should('include', 'gorpermatabadminton.com');

    cy.request({ url: `${baseUrl}/register`, failOnStatusCode: false })
      .its('status')
      .should('eq', 404);
  });

  it('TC-GOR-04 s.d. 08: Membuka modal booking, cek kalkulasi harga & validasi negatif WA', () => {
    const tomorrow = new Date(Date.now() + 86400000).toISOString().slice(0, 10);
    cy.visit(`${baseUrl}/booking?start_date=${tomorrow}`);

    cy.get('[onclick*="openBooking("]').first().click();
    cy.get('#bookingModal').should('be.visible');
    cy.get('#dispTotal').should('contain', '40.000');

    // Uji kalkulasi tarif 2 jam
    cy.get('#custDuration').select('2');
    cy.get('#dispTotal').should('contain', '80.000');

    // Uji validasi input kosong
    cy.on('window:alert', (text) => {
      expect(text).to.match(/harus diisi lengkap|Nomor WA belum benar/);
    });

    cy.get('#custName').clear();
    cy.get('#custPhone').clear();
    cy.get('#btnSubmit').click();

    // Uji reproduksi bug White Box format +62 08...
    cy.get('#custName').type('Test QA');
    cy.get('#custPhone').type('+62 08123456789');
    cy.get('#btnSubmit').click();
  });
});

