// on load 

document.addEventListener('DOMContentLoaded', function() {
    // get class .toggle 
    var toggles = document.getElementsByClassName('toggle');

    // add a button as the first child of the toggle class 
    for (var i = 0; i < toggles.length; i++) {
        var toggle = toggles[i];

        var button = document.createElement('button');
        button.classList.add('toggle-button');
        button.innerHTML = '+ show code';
        button.id = 'toggle-button-' + i;
        toggle.insertBefore(button, toggle.firstChild);

        // get `pre` tag right after the button
        codeBlock = button.nextElementSibling;
        codeBlock.classList.add('hidden');
        codeBlock.style.marginTop = "-20px";
        codeBlock.id = "codeBlock" + i;

    }


    for (var i = 0; i < toggles.length; i++) {
        let button = document.getElementById('toggle-button-' + i);
        // add event listener to button
        // when button is clicked, toggle the code codeBlock 
        button.addEventListener('click', function() {
            var _cb = document.getElementById("codeBlock" + button.id.split("-")[2]);
            console.log(button.id);
            console.log(_cb);
            _cb.classList.toggle('hidden');

            // change pre content to "-" or "+" depending on the state of the codeBlock
            if (_cb.classList.contains('hidden')) {
                button.innerHTML = '+ show code';
            } else {
                button.innerHTML = ' - hide code';
            }
        });
    }
});  
