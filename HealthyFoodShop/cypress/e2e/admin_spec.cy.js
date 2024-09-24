describe('Admin Panel', () => {
  beforeEach(() => {
    cy.login('user', 'user');
  });

  it('should login the admin successfully', () => {
    cy.url().should('include', '/admin/');
    cy.contains('Site administration').should('exist');
  });

  it('Navigates to Categories and Lists Them', () => {
    cy.visit('/admin/HealthyFoodApp/category/');

    cy.contains('Select category to change').should('be.visible');
    cy.get('table').should('exist');
  });
  it('Navigates to Products and Lists Them', () => {
    cy.visit('/admin/HealthyFoodApp/product/');

    cy.contains('Select product to view').should('be.visible');
    cy.get('table').should('exist');
  });
  it('Navigates to Clients and Lists Them', () => {
    cy.visit('/admin/HealthyFoodApp/client/');

    cy.contains('Select client to change').should('be.visible');
    cy.get('table').should('exist');
  });
  it('Navigates to Sales and Lists Them', () => {

    cy.visit('/admin/HealthyFoodApp/sale/');

    cy.contains('Select sale to change').should('be.visible');
    cy.get('table').should('exist');
  });
});