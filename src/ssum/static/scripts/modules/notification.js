export class NotificationManager {
    // Class responsible for announcing notifications to the user.

    static announceStatus() {
        // Based on notification metadata from <head>,
        // create notification elements and add them to an aria-live region in the header.
        // Used for general notifications that don't relate to
        // particular elements on the page.
        
        let notificationFound = false;
        for (let el of document.getElementsByTagName('meta')) {
            if (el.name.endsWith('notif')) {

                if (!notificationFound) {
                    document.getElementById('notifications').hidden = false;
                    notificationFound = true;
                }

                let index = el.name.indexOf('-');
                let category = el.name.substring(0, index);
                let content = el.content;

                // Error notifications go in an assertive live region.
                // Other notifications go in a polite live region.
                // This indicates priority to screen readers.
                let parentElem;
                let className = category;
                if (category == 'error') {
                    parentElem = document.getElementById('assertive-header-notifications');
                    className = 'bad'
                }
                else {
                    parentElem = document.getElementById('polite-header-notifications');
                    if (category == 'success') {
                        className = 'ok'
                    }
                }

                // Create and append notification element.
                let notifElem = document.createElement('p');
                notifElem.textContent = content;
                notifElem.className = 'box ' + className;
                parentElem.appendChild(notifElem);
            }
        }
    }

    static announceFormErrors() {
        // Focus the error region for the form.
        // NOTE: this could also be changed to add aria-invalid and aria-describedby
        // for the errors, simplifying the form rendering logic in utils/form_macros.html,
        // although that probably wouldn't be worth the time spent refactoring.

        if (document.querySelector('[aria-invalid]')) {
            let errorRegion = document.getElementById("form-errors");
            errorRegion.focus();
        }
    }
}