const apiBaseUrl = 'http://127.0.0.1:8000'; // Remplacez par l'URL de votre API si nécessaire

// Fonction pour ajouter une catégorie
async function addCategory() {
    const name = document.getElementById('categoryName').value;
    const description = document.getElementById('categoryDescription').value;
    const author = document.getElementById('categoryAuthor').value;

    if (!name) {
        alert("Le nom de la catégorie est requis !");
        return;
    }

    try {
        const response = await fetch(`${apiBaseUrl}/categories/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ name, description, author })
        });

        if (!response.ok) {
            throw new Error("Erreur lors de l'ajout de la catégorie");
        }

        alert("Catégorie ajoutée avec succès !");
        fetchCategories(); // Rafraîchir la liste
    } catch (error) {
        alert(error.message);
    }
}

// Fonction pour récupérer et afficher toutes les catégories
async function fetchCategories() {
    try {
        const response = await fetch(`${apiBaseUrl}/categories/`);
        if (!response.ok) {
            throw new Error("Erreur lors de la récupération des catégories");
        }

        const categories = await response.json();
        const categoriesList = document.getElementById('categoriesList');
        categoriesList.innerHTML = ''; // Vider la liste avant de la remplir

        categories.forEach(category => {
            const categoryElement = document.createElement('div');
            categoryElement.classList.add('category');
            categoryElement.innerHTML = `
                <h3>${category.name}</h3>
                <p>${category.description || 'Aucune description'}</p>
                <p>${category.author}</p>
                <button class="delete" onclick="deleteCategory(${category.id})">Supprimer</button>
            `;
            categoriesList.appendChild(categoryElement);
        });
    } catch (error) {
        alert(error.message);
    }
}

// Fonction pour supprimer une catégorie
async function deleteCategory(categoryId) {
    if (!confirm("Êtes-vous sûr de vouloir supprimer cette catégorie ?")) {
        return;
    }

    try {
        const response = await fetch(`${apiBaseUrl}/categories/${categoryId}`, {
            method: 'DELETE'
        });

        if (!response.ok) {
            throw new Error("Erreur lors de la suppression de la catégorie");
        }

        alert("Catégorie supprimée avec succès !");
        fetchCategories(); // Rafraîchir la liste
    } catch (error) {
        alert(error.message);
    }
}

// Charger les catégories au démarrage de la page
window.onload = fetchCategories;
