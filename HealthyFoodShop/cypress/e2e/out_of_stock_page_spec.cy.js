describe('Out of Stock Page Tests', () => {
    beforeEach(() => {
        cy.visit('/out_of_stock/');
    });

    it('should display the Out of stock header', () => {
        cy.get('h1.fw-bold').should('have.text', 'Out of stock');
        cy.get('.border-success').should('have.css', 'border-bottom-width', '3px');
    });

    it('should display product cards with correct details', () => {
        cy.get('.row.mt-5.g-4.gy-4 .col-3').should('have.length.greaterThan', 0);

        cy.get('.col-3').each(($el) => {
            cy.get($el).find('img.card-img-top').should('have.attr', 'src').and('include', '/data/');

            cy.get($el).find('p').first().should('not.be.empty');

            cy.get($el).find('p.fw-bold').should('contain.text', '$');
        });
    });

    it('should display and submit the form correctly', () => {
        cy.get('form').should('exist');

        cy.get('form').within(() => {
            cy.get('input, select, textarea').should('exist');
            cy.get('button[type="submit"]').should('exist').and('have.text', 'Submit');
        });

        cy.get('input[name="name"]').type('Sample Product');

        cy.get('textarea[name="description"]').type('This is a sample product description.');

        cy.get('select[name="category"]').select('Fruit'); // Replace with actual category

        cy.get('input[name="price"]').type('19.99');

        cy.get('input[name="quantity"]').type('10');

        cy.get('button[type="submit"]').click();

        cy.url().should('include', '/out_of_stock/');
    });

    it('should display footer sections correctly', () => {
        cy.get('.col-4').eq(0).within(() => {
            cy.get('p.fw-bold').should('have.text', 'FINKI Exam');
            cy.get('p').should('contain.text', 'Organization')
                        .and('contain.text', 'Departments')
                        .and('contain.text', 'Contact');
        });

        cy.get('.col-4').eq(1).within(() => {
            cy.get('p.fw-bold').should('have.text', 'Studies');
            cy.get('p').should('contain.text', 'Bachelors')
                        .and('contain.text', 'Masters')
                        .and('contain.text', 'PhD');
        });

        cy.get('.col-4').eq(2).within(() => {
            cy.get('p.fw-bold').should('have.text', 'Staff');
            cy.get('p').should('contain.text', 'Administrative')
                        .and('contain.text', 'Testing');
        });
    });
});
