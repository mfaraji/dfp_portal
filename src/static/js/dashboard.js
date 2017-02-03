var Dashboard = function() {

    return {

        init: function() {
            console.log('Dashboard Initialization');
        }
    };

}();

if (App.isAngularJsApp() === false) {
    console.log(App.isAngularJsApp())
    jQuery(document).ready(function() {
        Dashboard.init(); // init metronic core componets
    });
}