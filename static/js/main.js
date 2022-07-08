/*
    General scripts to apply to all modules
*/

// Prevents ddos attacks related to spamming f5
if(window.history.replaceState){
    window.history.replaceState(null, null, window.location.href);
}