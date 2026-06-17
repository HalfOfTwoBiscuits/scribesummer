import { NotificationManager } from './modules/notification.js';
import { FilterManager } from './modules/filter.js';
import { SearchManager } from './modules/search.js';

class Base {
    static loadPage() {
        // Move notifications into an ARIA live region.
        NotificationManager.announceStatus();
        NotificationManager.announceFormErrors();

        // If the page has a search widget, create a JS object to manage it.
        if (document.getElementById('searchBar') && document.getElementById('presetList')) {
            let sm = new SearchManager();
            window.searchManager = sm;
        }

        // Likewise with the subscription filtering.
        if (document.getElementById('categorySelect') && document.getElementById('subscriptionList')) {
            let fm = new FilterManager();
            window.filterManager = fm;
        }
    }
}

// Add Base to the namespace for the HTML document.
// This must be done explicitly because JS with type `module` isn't
// added to the namespace until the HTML is completely loaded, which may
// not be the case at the time of the `onload` event that calls `Base.loadPage()`.
window.Base = Base;