/***
Inspire AngularJS App Main Script
***/

var InspireApp = angular.module("InspireApp", [
    "ui.router", 
    "ui.bootstrap", 
    "oc.lazyLoad",  
    "ngSanitize",
    'blockUI',
]); 

InspireApp.config(['$interpolateProvider',
    function($interpolateProvider) {
        $interpolateProvider.startSymbol('{[');
        $interpolateProvider.endSymbol(']}');
    }
]);

/* Configure ocLazyLoader(refer: https://github.com/ocombe/ocLazyLoad) */
InspireApp.config(['$ocLazyLoadProvider', function($ocLazyLoadProvider) {
    $ocLazyLoadProvider.config({
        // global configs go here
    });
}]);

//AngularJS v1.3.x workaround for old style controller declarition in HTML
InspireApp.config(['$controllerProvider', function($controllerProvider) {
  // this option might be handy for migrating old apps, but please don't use it
  // in new ones!
  $controllerProvider.allowGlobals();
}]);

/********************************************
 END: BREAKING CHANGE in AngularJS v1.3.x:
*********************************************/

InspireApp.factory('settings', ['$rootScope', function($rootScope) {
    // supported languages
    var settings = {
        layout: {
            pageSidebarClosed: false, // sidebar menu state
            pageContentWhite: true, // set page content layout
            pageBodySolid: false, // solid body color state
            pageAutoScrollOnLoad: 1000 // auto scroll to top on page load
        },
        assetsPath: '../assets',
        globalPath: '../assets/global',
        layoutPath: '../assets/layouts/layout2',
    };

    $rootScope.settings = settings;

    return settings;
}]);

InspireApp.controller('AppController', ['$scope', '$rootScope', function($scope, $rootScope) {
    $scope.$on('$viewContentLoaded', function() {
        console.log('Main controller is loaded');
        //App.initComponents(); // init core components
        // Layout.init(); //  Init entire layout(header, footer, sidebar, etc) on page load if the partials included in server side instead of loading with ng-include directive 
    });
}]);


InspireApp.controller('HeaderController', ['$scope', function($scope) {
    $scope.$on('$includeContentLoaded', function() {
        Layout.initHeader(); // init header
    });
}]);

InspireApp.controller('SidebarController', ['$state', '$scope', function($state, $scope) {
    $scope.$on('$includeContentLoaded', function() {
        Layout.initSidebar($state); // init sidebar
    });
}]);

InspireApp.controller('QuickSidebarController', ['$scope', function($scope) {    
    $scope.$on('$includeContentLoaded', function() {
       setTimeout(function(){
            QuickSidebar.init(); // init quick sidebar        
        }, 2000)
    });
}]);

InspireApp.controller('ThemePanelController', ['$scope', function($scope) {    
    $scope.$on('$includeContentLoaded', function() {
        Demo.init(); // init theme panel
    });
}]);

InspireApp.controller('FooterController', ['$scope', function($scope) {
    $scope.$on('$includeContentLoaded', function() {
        Layout.initFooter(); // init footer
    });
}]);

InspireApp.config(['$stateProvider', '$urlRouterProvider', function($stateProvider, $urlRouterProvider) {
    // Redirect any unmatched url
    $urlRouterProvider.otherwise("/dashboard");  

    $stateProvider

        // Dashboard
        .state('dashboard', {
            url: "/dashboard",
            templateUrl: "views/dashboard",            
            data: {pageTitle: 'Admin Dashboard Template'},
            controller: "DashboardController",
            resolve: {
                deps: ['$ocLazyLoad', function($ocLazyLoad) {
                    return $ocLazyLoad.load({
                        name: 'InspireApp',
                        insertBefore: '#ng_load_plugins_before', // load the above css files before a LINK element with this ID. Dynamic CSS files must be loaded between core and theme css files
                        files: [
                            '/static/js/datatable.js',
                            '/static/js/dashboard.js',
                            '/static/js/controllers/DashboardController.js',
                        ] 
                    });
                }]
            }
        })

    // // Aduience Page
    // .state('audience', {
    //     url: "/audience",
    //     templateUrl: "views/audience",            
    //     data: {pageTitle: 'Blank Page Template'},
    //     controller: "BlankController",
    //     resolve: {
    //         deps: ['$ocLazyLoad', function($ocLazyLoad) {
    //             return $ocLazyLoad.load({
    //                 name: 'InspireApp',
    //                 insertBefore: '#ng_load_plugins_before', // load the above css files before a LINK element with this ID. Dynamic CSS files must be loaded between core and theme css files
    //                 files: [
    //                     '/static/js/controllers/BlankController.js'
    //                 ] 
    //             });
    //         }]
    //     }
    // })

        // Add Report Page
        .state('addreport', {
            url: "/add",
            templateUrl: "views/addreport",            
            data: {pageTitle: 'Add New Report'},
            controller: "AddReportController",
            resolve: {
                deps: ['$ocLazyLoad', function($ocLazyLoad) {
                    return $ocLazyLoad.load({
                        name: 'InspireApp',
                        insertBefore: '#ng_load_plugins_before', // load the above css files before a LINK element with this ID. Dynamic CSS files must be loaded between core and theme css files
                        files: [
                            '/static/libs/bootstrap-datepicker/dist/css/bootstrap-datepicker3.min.css',
                            '/static/libs/bootstrap-datepicker/dist/js/bootstrap-datepicker.min.js',
                            '/static/libs/angular-ui-select/dist/select.min.js',
                            '/static/libs/angular-ui-select/dist/select.min.css',
                            '/static/libs/angular-bootstrap-multiselect/dist/angular-bootstrap-multiselect.min.js',
                            '/static/js/controllers/AddReportController.js'
                        ] 
                    });
                }]
            }
        })

        // View Report
        .state('view', {
            url: "/dashboard/view/:reportId",
            templateUrl: "views/report_datatable",            
            data: {pageTitle: 'View Report'},
            controller: "ViewReportController",
            resolve: {
                deps: ['$ocLazyLoad', function($ocLazyLoad) {
                    return $ocLazyLoad.load({
                        name: 'InspireApp',
                        insertBefore: '#ng_load_plugins_before', // load the above css files before a LINK element with this ID. Dynamic CSS files must be loaded between core and theme css files
                        files: [
                            '/static/js/controllers/ViewReportController.js'
                        ] 
                    });
                }]
            }
        })

        .state('editReport', {
            url: "/edit/:reportId",
            templateUrl: "views/addreport",            
            data: {pageTitle: 'Edit Report'},
            controller: "AddReportController",
            resolve: {
                deps: ['$ocLazyLoad', function($ocLazyLoad) {
                    return $ocLazyLoad.load({
                        name: 'InspireApp',
                        insertBefore: '#ng_load_plugins_before', // load the above css files before a LINK element with this ID. Dynamic CSS files must be loaded between core and theme css files
                        files: [
                            '/static/libs/bootstrap-datepicker/dist/css/bootstrap-datepicker3.min.css',
                            '/static/libs/bootstrap-datepicker/dist/js/bootstrap-datepicker.min.js',
                            '/static/libs/angular-ui-select/dist/select.min.js',
                            '/static/libs/angular-ui-select/dist/select.min.css',
                            '/static/libs/angular-bootstrap-multiselect/dist/angular-bootstrap-multiselect.min.js',
                            '/static/js/controllers/AddReportController.js'
                        ] 
                    });
                }]
            }
        })

}]);

/* Init global settings and run the app */
InspireApp.run(["$rootScope", "settings", "$state", function($rootScope, settings, $state) {
    $rootScope.$state = $state; // state to be accessed from view
    $rootScope.$settings = settings; // state to be accessed from view
}]);