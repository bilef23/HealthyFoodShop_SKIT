describe('Home Page', () => {
    it('should load the home page', () => {
        cy.visit('http://localhost:8000/index');

        cy.get('div[style*="background"]').should('exist');

        cy.contains('FRUIT FRESH').should('exist');

        cy.contains('Shop now').should('be.visible').and('have.attr', 'href', '/out_of_stock/');
    });
});

describe('Dropdown Menu', () => {
    it('should open the dropdown and display categories', () => {
        cy.visit('http://localhost:8000/index');

        cy.get('.dropdown-toggle').click();

        cy.get('.dropdown-menu').should('be.visible');

        cy.get('.dropdown-item').should('have.length.greaterThan', 0);

        cy.get('.dropdown-item').first().should('contain', 'Fruit');
    });
});

describe('Banner Section', () => {
    it('should display banner content', () => {
        cy.visit('http://localhost:8000/index');

        cy.contains('FRUIT FRESH').should('exist');

        cy.contains('100% Organic').should('exist');

        cy.get('a[href="/out_of_stock/"]').should('contain', 'Shop now').click();

        cy.url().should('include', '/out_of_stock');
    });
});

describe('Blog Section', () => {
    it('should display blog cards with content', () => {
        cy.visit('http://localhost:8000/index');

        cy.get('.card').should('have.length', 3);

        cy.get('.card').first().within(() => {
            cy.get('.card-title').should('contain', 'Cooking tips make cooking simple');
            cy.get('.card-text').should('contain', 'Lorem ipsum dolor sit amet');
            cy.get('img').should('have.attr', 'src').and('include', 'blog-1.jpg');
        });
    });
});

describe('Footer Section', () => {
    it('should display the footer with correct sections', () => {
        cy.visit('http://localhost:8000/index');

        cy.contains('FINKI Exam').should('exist');

        cy.contains('Studies').should('exist');
        cy.contains('Bachelors').should('exist');

        cy.contains('Staff').should('exist');
        cy.contains('Administrative').should('exist');
    });
});

describe('Responsive Layout', () => {
    it('should display the layout correctly on small screens', () => {
        cy.visit('http://localhost:8000/index');

        cy.viewport('iphone-XS');

        cy.get('.dropdown-toggle').should('be.visible');
        cy.get('div[style*="background"]').should('exist');
    });
});
