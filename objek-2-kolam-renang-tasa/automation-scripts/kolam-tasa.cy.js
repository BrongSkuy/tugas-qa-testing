// Contoh Test Script Cypress (Sesuai Materi Automation Testing 14 Nov 2026)
// Objek 2: Website Kolam Renang TASA Pamulang (https://www.kolamtasa.com/)
// Non-destruktif: menguji validasi wizard, blog pagination, dan form kontak tanpa submit ke backend

describe('Kolam Renang TASA Pamulang - Non-Destructive QA Suite', () => {
  const baseUrl = 'https://www.kolamtasa.com';

  beforeEach(() => {
    // Pengaman agar pengujian berulang tidak pernah mengirim POST ke Server Action
    cy.intercept('POST', '**', { statusCode: 400, body: { blocked: true } }).as('blockedPost');
  });

  it('TC-TASA-01 & 02: Cek halaman utama, footer mati, dan route 404', () => {
    cy.visit(baseUrl);
    cy.contains('Hak Cipta 2023 - Kolam Renang TASA').should('exist');
    cy.get('footer a').should('not.contain.text', 'Privacy');

    cy.request({ url: `${baseUrl}/privacy`, failOnStatusCode: false })
      .its('status')
      .should('eq', 404);
  });

  it('TC-TASA-03: Verifikasi form /kontak tidak memiliki action/method', () => {
    cy.visit(`${baseUrl}/kontak`);
    cy.get('form')
      .should('not.have.attr', 'action')
      .and('not.have.attr', 'method');
  });

  it('TC-TASA-04 & 05: Uji validasi negatif & transisi step 1 -> step 2 pada wizard /lesrenang', () => {
    cy.visit(`${baseUrl}/lesrenang`);
    cy.contains('1/20').should('be.visible');
    cy.contains('Siapa nama lengkap muridnya?').should('be.visible');

    // Klik Lanjut tanpa mengisi nama
    cy.contains('button', 'Lanjut').click();
    cy.contains('Nama muridnya belum diisi.').should('be.visible');

    // Isi nama murid lalu lanjut ke Step 2
    cy.get('input[placeholder="Nama sesuai akta"]').type('Calon Murid QA');
    cy.contains('button', 'Lanjut').click();
    cy.contains('Nama panggilannya?').should('be.visible');

    // Uji Step 2 kosong
    cy.contains('button', 'Lanjut').click();
    cy.contains('Nama panggilannya belum diisi.').should('be.visible');
  });

  it('TC-TASA-09: Cek boundary pagination /blog/halaman/2 (200) vs /blog/halaman/5 (404)', () => {
    cy.visit(`${baseUrl}/blog`);
    cy.get('input[type="search"]').should('not.exist');
    cy.request(`${baseUrl}/blog/halaman/2`).its('status').should('eq', 200);
    cy.request({ url: `${baseUrl}/blog/halaman/5`, failOnStatusCode: false })
      .its('status')
      .should('eq', 404);
  });
});
