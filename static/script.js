function basculerTache(id) {
    fetch('/cocher/' + id, { method: 'POST' })
        .then(reponse => reponse.json())
        .then(data => {
            const texte = document.getElementById('texte-tache-' + id);
            const bouton = document.getElementById('bouton-tache-' + id);

            if (data.fait) {
                texte.innerHTML = '<s>' + texte.textContent.trim() + '</s>';
                bouton.textContent = 'Décocher';
            } else {
                texte.innerHTML = texte.textContent.trim();
                bouton.textContent = 'Cocher';
            }
        });
}