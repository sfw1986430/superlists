window.Superlists = {};
window.Superlists.initialize = function () {
    $('input[name="text"]').on('keypress', function () {
        $('.is-invalid').hide();
    });
};