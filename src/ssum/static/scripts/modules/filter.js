export class FilterManager {
    // Class responsible for managing the filtering of subscriptions by category.

    #categoryElem;
    #resultListElem;
    #resultAreaElem;
    #showMoreButtonElem;
    #noResultsElem;
    #matchingResults;
    #initialNumResults;
    #maxResults;
    
    constructor() {
        this.#categoryElem = document.getElementById("categorySelect");
        this.#resultListElem = document.getElementById("subscriptionList");
        this.#resultAreaElem = document.getElementById("matchingResults");
        this.#showMoreButtonElem = document.getElementById("showMoreButton");
        this.#noResultsElem = document.getElementById("noResultsMessage");

        this.#initialNumResults = this.resultListElem.dataset.initialNumResults;
        this.#maxResults = 0;

        // On initalisation, find matching results and display the first lot.
        this.#findMatchingResults();
        this.showMore();
    }

    changeFilter() {
        // Filter results so only those that match the criteria are shown.
        // Called on choosing a category.

        this.#findMatchingResults();
        this.#filterResults();
        this.#toggleShowMore();
    }

    showMore() {
        // Increase the maximum number of results by the number that were initially present.
        // Called on pressing 'Show more'.

        this.#maxResults += this.#initialNumResults;
        this.#filterResults();
        this.#toggleShowMore();
    }

    #findMatchingResults() {
        // Return list of <li> elements representing results
        // matching the selected category.

        // Retrieve selected category.
        let selectedCategory = this.#categoryElem.options[this.#categoryElem.selectedIndex].value;
        selectedCategory = parseInt(selectedCategory);

        let allResultElems = this.#resultListElem.children;
        let categories;
        
        this.#matchingResults = new Array();
        for (let resultElem of allResultElems) {
            // Parse JSON array of categories for each result.
            categories = JSON.parse(resultElem.dataset.filterCategories);

            // Results should appear if the selected category is within the array.
            if (categories.includes(selectedCategory)) {
                this.#matchingResults.push(resultElem);
            }
        }
    }

    #filterResults() {
        // Filter the list of results.
        // Only results matching the currently selected category should be shown,
        // up to a total amount based on how many times the 'Show more' button has been clicked.

        let allResultElems = this.#resultListElem.children;
        let numResults = allResultElems.length;

        // Number of results to show is limited by the amount of matching results.
        let maxResults = Math.min(this.#maxResults, this.#matchingResults.length);

        if (maxResults === 0) {
            // If there are no results then show a message explaining this.
            this.#resultAreaElem.hidden = true;
            this.#noResultsElem.hidden = false;
        }
        else {
            this.#resultAreaElem.hidden = false;
            this.#noResultsElem.hidden = true;
            
            // Iterate over all results.
            let numShown = 0;
            for (let i = 0; i < numResults; i++) {
                let resultElem = allResultElems[i];

                // If the result matches and we haven't reached the maximum,
                // show the element. Otherwise hide it.
                if (numShown < maxResults && this.#matchingResults.includes(resultElem)) {
                    resultElem.hidden = false;
                    resultElem.disabled = false;
                    numShown += 1;
                }
                else {
                    resultElem.hidden = true;
                    resultElem.disabled = true;
                }
            }
        }
    }

    #toggleShowMore() {
        // Helper method that shows or hides the 'Show more' button
        // depending on whether all valid results are shown.

        let numMatchingResults = this.#matchingResults.length;

        if (this.#maxResults >= numMatchingResults) {
            this.#showMoreButtonElem.hidden = true;
            this.#showMoreButtonElem.disabled = true;
        }
        else {
            this.#showMoreButtonElem.hidden = false;
            this.#showMoreButtonElem.disabled = false;
        }
    }
}