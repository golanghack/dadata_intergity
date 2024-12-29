document.addEventListener('DOMContentLoaded', function() {
    const addressInput = document.getElementById('id_address');
    if (addressInput) {
        addressInput.addEventListener('input', function() {
            const query = this.value;
            if (query.length < 3) return;
            const url = "https://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest/address";
            const token = "013c81e017bc205abdee1b88844fd28d860578ee";
            const options = {
                method: "POST",
                mode: "cors",
                headers: {
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                    "Authorization": "Token " + token
                },
                body: JSON.stringify({ query: query })
            };
            fetch(url, options)
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.json();
                })
                .then(data => {
                    let suggestionsContainer = document.querySelector('.dadata-suggestions');
                    if (!suggestionsContainer) {
                        suggestionsContainer = document.createElement('div');
                        suggestionsContainer.classList.add('dadata-suggestions');
                        addressInput.parentNode.appendChild(suggestionsContainer);
                    }
                    suggestionsContainer.innerHTML = '';
                    if (data.suggestions && data.suggestions.length > 0) {
                        data.suggestions.forEach(suggestion => {
                            const suggestionItem = document.createElement('div');
                            suggestionItem.textContent = suggestion.value;
                            suggestionItem.classList.add('suggestion-item');
                            suggestionItem.addEventListener('click', () => {
                                addressInput.value = suggestion.value;
                                suggestionsContainer.innerHTML = '';
                            });
                            suggestionsContainer.appendChild(suggestionItem);
                        });
                    }
                })
                .catch(error => {
                    console.error('Ошибка при получении подсказок:', error);
                });
        });
        document.addEventListener('click', function(event) {
            const suggestionsContainer = document.querySelector('.dadata-suggestions');
            if (suggestionsContainer && 
                !suggestionsContainer.contains(event.target) && 
                event.target !== addressInput) {
                suggestionsContainer.innerHTML = '';
            }
        });
    }
});