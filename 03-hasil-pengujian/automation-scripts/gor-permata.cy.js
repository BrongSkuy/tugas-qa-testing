// Test Script Cypress E2E (ISO/IEC/IEEE 29119-2:2021 & 29119-5)
// Objek: Portal Booking GOR Permata Badminton Hall
// Catatan: Non-destruktif - memblokir POST **/bookings/store via cy.intercept

describe('GOR Permata Badminton Hall - Black Box QA Suite (TC-BB-01..19)', () => {
  const baseUrl = 'https://gorpermatabadminton.com';

  beforeEach(() => {
    // Pengaman jaringan agar tidak pernah membuat booking nyata di database UMKM
    cy.intercept('POST', '**/bookings/store', {
      statusCode: 400,
      body: { success: false, message: 'Blocked in QA test mode' },
    }).as('blockedBookingStore');
  });

  it('TC-BB-01 & TC-BB-02: Memastikan rute publik aktif dan mencatat /register 404', () => {
    const routes = ['/', '/booking', '/login', '/fasilitas/lapangan', '/fasilitas/umum', '/fasilitas/tunggu', '/fasilitas/parkir'];
    routes.forEach((route) => {
      cy.request(baseUrl + route).its('status').should('eq', 200);
    });

    cy.request({ url: `${baseUrl}/register`, failOnStatusCode: false })
      .its('status')
      .should('eq', 404);
  });

  it('TC-BB-03, 06, 07, 08, 10, 11, 14, 16, 19: Modal, Tarif 1..5 Jam, BVA WA, & Close Reset', () => {
    const tomorrow = new Date(Date.now() + 86400000).toISOString().slice(0, 10);
    cy.visit(`${baseUrl}/booking?start_date=${tomorrow}`);
    cy.get('#jumpDate').should('have.value', tomorrow);

    cy.get('[onclick*="openBooking("]').first().click();
    cy.get('#bookingModal').should('be.visible');
    cy.get('#dispTotal').should('contain', '40.000');

    // TC-BB-07: Cek seluruh durasi 1..5 jam
    const expected = { '1': '40.000', '2': '80.000', '3': '120.000', '4': '160.000', '5': '200.000' };
    Object.entries(expected).forEach(([dur, price]) => {
      cy.get('#custDuration').select(dur);
      cy.get('#dispTotal').should('contain', price);
    });
    cy.get('#custDuration').select('1');

    cy.on('window:alert', (text) => {
      expect(text).to.match(/harus diisi lengkap|Nomor WA belum benar|tutup jam 00:00/);
    });

    // TC-BB-08: Input kosong (stop di klien)
    cy.get('#custName').clear();
    cy.get('#custPhone').clear();
    cy.get('#btnSubmit').click();

    // TC-BB-10, 11, 14, 16: EP/BVA WA tidak valid & repro +62 08...
    cy.get('#custName').type('Test QA');
    ['12345', '081234567', '08123456789012', '+62 08123456789'].forEach((badWa) => {
      cy.get('#custPhone').clear().type(badWa);
      cy.get('#btnSubmit').click();
    });

    // TC-BB-19: Tutup modal & pastikan form reset
    cy.window().then((win) => win.closeModal());
    cy.get('#bookingModal').should('not.be.visible');
    cy.get('#custName').should('have.value', '');
    cy.get('#custPhone').should('have.value', '');
  });

  it('TC-BB-17: BVA Batas Jam Tutup 00:00 pada slot 22:00 + 3 Jam', () => {
    const tomorrow = new Date(Date.now() + 86400000).toISOString().slice(0, 10);
    cy.visit(`${baseUrl}/booking?start_date=${tomorrow}`);

    cy.get('[onclick*="openBooking(\'22:00\'"]').first().click();
    cy.get('#custName').type('Test QA');
    cy.get('#custPhone').type('08123456789');
    cy.get('#custDuration').select('3');

    cy.on('window:alert', (text) => {
      expect(text).to.include('tutup jam 00:00');
    });
    cy.get('#btnSubmit').click();
  });
});
